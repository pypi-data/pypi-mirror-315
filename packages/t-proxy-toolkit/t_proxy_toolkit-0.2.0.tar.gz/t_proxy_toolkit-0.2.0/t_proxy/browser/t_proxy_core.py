import json
import time

from fake_useragent import UserAgent
from retry import retry
from RPA.Browser.Selenium import Selenium
from SeleniumLibrary.errors import NoOpenBrowser

from t_proxy.exceptions import ExtensionNotConnectedException, IPAddressValidationException
from t_proxy.utils.logger import logger


class BrowserProxyCore:
    """Base class for browser proxy implementations.

    Provides core functionality for proxy configuration, browser management,
    and IP validation across different browser types.
    """

    def __init__(self, user: str, password: str, port: int, host: str):
        """Initialize core proxy configuration.

        Args:
            user (str): Proxy username for authentication
            password (str): Proxy password for authentication
            port (int): Proxy port number
            host (str): Proxy host address

        Attributes:
            id (str): Extension ID after installation
            uuid (str): Extension UUID for URL generation
            browser (Selenium): Selenium browser instance
            user_agent (UserAgent): User agent generator for Windows platforms
            initial_ip (str): Original IP address before proxy connection
        """
        self.id = ""
        self.uuid = ""
        self.user = user
        self.password = password
        self.port = port
        self.host = host
        self.browser = Selenium()
        self.user_agent = UserAgent(os="windows", min_percentage=1.3)
        self.initial_ip = self.__get_current_ip()
        self._chrome_extension_url = "chrome-extension://{}/popup.html"
        self._chrome_extension_url_options = "chrome-extension://{}/options.html"
        self._firefox_extension_url = "moz-extension://{}/content/popup.html"
        self._firefox_extension_url_options = "moz-extension://{}/content/options.html"

    def is_browser_open(self) -> bool:
        """Check if browser instance is currently active.

        Returns:
            bool: True if browser is open and driver exists, False otherwise
        """
        try:
            return self.browser.driver is not None
        except NoOpenBrowser:
            return False

    def __get_current_ip(self):
        """Retrieve current IP address using multiple services.

        Attempts to get IP from httpbin.org first, falls back to ifconfig.me if needed.
        Manages browser lifecycle if no browser is currently open.

        Returns:
            str: Current IP address

        Note:
            Will temporarily open and close browser if none is currently active
        """
        logger.debug("Getting current IP...")

        driver_is_alive = self.is_browser_open()
        close_browser = False

        if not driver_is_alive:
            self.browser.open_available_browser()
            close_browser = True

        try:
            self.browser.go_to("https://httpbin.org/ip")
            self.browser.wait_until_element_is_visible("//pre")
            ip_literal = self.browser.get_text("//pre")
            ip_json = json.loads(ip_literal)
            ip = ip_json["origin"]
        except Exception as ex:
            logger.exception(ex)
            logger.warning("Failed to get IP from Oxylabs page. Using ifconfig.me as a backup.")
            self.browser.go_to("https://ifconfig.me/")
            self.browser.wait_until_element_is_visible("//td[@id='ip_address_cell']")
            ip = self.browser.get_text("//td[@id='ip_address_cell']")
        if close_browser:
            self.browser.close_browser()

        return ip

    @property
    def chrome_extension_url(self):
        """Get Chrome extension popup URL template.

        Returns:
            str: URL template for Chrome extension popup
        """
        return self._chrome_extension_url

    @property
    def chrome_extension_url_options(self):
        """Get Chrome extension options URL template.

        Returns:
            str: URL template for Chrome extension options page
        """
        return self._chrome_extension_url_options

    @property
    def firefox_extension_url(self):
        """Get Firefox extension popup URL template.

        Returns:
            str: URL template for Firefox extension popup
        """
        return self._firefox_extension_url

    @property
    def firefox_extension_url_options(self):
        """Get Firefox extension options URL template.

        Returns:
            str: URL template for Firefox extension options page
        """
        return self._firefox_extension_url_options

    @retry(ExtensionNotConnectedException, tries=3, delay=5)
    def login_on_firefox_extension(self, url1: str, url2: str):
        """Configure and authenticate Firefox extension.

        Args:
            url1 (str): Extension popup URL
            url2 (str): Extension options URL

        Raises:
            ExtensionNotConnectedException: If extension fails to connect to proxy
            after configuration

        Note:
            Retries up to 3 times with 5-second delay between attempts
        """
        logger.debug("Logging in to Oxylabs extension...")

        proxies_xpath = '//label[@data-i18n="proxies"]'
        add_xpath = '//button[@data-i18n="add"]'
        name_xpath = '//input[@data-id="title"]'
        select_xpath = "//select[@data-id='type']"
        hostname_xpath = '//input[@data-id="hostname"]'
        port_xpath = '//input[@data-id="port"]'
        username_xpath = '//input[@data-id="username"]'
        password_xpath = '//input[@data-id="password"]'
        save_xpath = '//fieldset[@class="proxySection"]//button[@data-i18n="saveOptions"]'

        connect_xpath = '//span[@class="title" and contains(text(), "oxylabs")]'

        self.browser.go_to(url2)
        # self.browser.wait_until_element_is_visible(options_xpath)
        # self.browser.click_element_when_visible(options_xpath)

        self.browser.wait_until_element_is_visible(proxies_xpath)
        self.browser.click_element_when_visible(proxies_xpath)
        time.sleep(3)

        self.browser.wait_until_element_is_visible(add_xpath)
        self.browser.click_element_when_visible(add_xpath)

        self.browser.wait_until_element_is_visible(name_xpath)
        self.browser.input_text(name_xpath, "oxylabs")
        self.browser.select_from_list_by_value(select_xpath, "https")
        self.browser.input_text(hostname_xpath, self.host)
        self.browser.input_text(port_xpath, str(self.port))
        self.browser.input_text(username_xpath, "user-" + self.user)
        self.browser.input_text(password_xpath, self.password)
        self.browser.click_element_when_visible(save_xpath)

        time.sleep(5)

        try:
            self.browser.go_to(url1)
            self.browser.wait_until_element_is_visible(connect_xpath, timeout=120)
            self.browser.click_element_when_visible(connect_xpath)
            self.browser.radio_button_should_be_set_to("server", f"{self.host}:{self.port}")
        except Exception as ex:
            if self.browser.does_page_contain_element(connect_xpath):
                logger.exception("Extension was not able to connect to the proxy.")
                raise ExtensionNotConnectedException("Extension was not able to connect to the proxy")
            else:
                logger.exception(ex)
                raise ex

    @retry(ExtensionNotConnectedException, tries=3, delay=5)
    def login_on_chrome_extension(self, url1: str, url2: str):
        """Configure and authenticate Chrome extension.

        Args:
            url1 (str): Extension popup URL
            url2 (str): Extension options URL

        Raises:
            ExtensionNotConnectedException: If extension fails to connect to proxy
            after configuration

        Note:
            Retries up to 3 times with 5-second delay between attempts
        """
        logger.debug("Logging in to Oxylabs extension...")
        new_proxy_xpath = '//button[contains(text(), "new proxy")]'
        name_xpath = '//input[contains(@name, "name")]'
        protocol_xpath = '//select[contains(@name, "protocol")]'
        hostname_xpath = '//input[contains(@name, "hostname")]'
        port_xpath = '//input[contains(@name, "port")]'
        username_xpath = '//input[contains(@name, "username")]'
        password_xpath = '//input[contains(@name, "password")]'
        save_changes_xpath = '//button[@type="submit"]'
        connect_button_xpath = '//button[contains(text(), "Connect")]'
        disconnect_button_xpath = '//button[contains(text(), "Disconnect")]'

        self.browser.go_to(url2)
        # self.browser.click_element_when_visible(new_proxy_xpath)
        self.browser.wait_until_element_is_visible(new_proxy_xpath)
        self.browser.input_text(name_xpath, "oxylabs")
        self.browser.select_from_list_by_value(protocol_xpath, "https")
        self.browser.input_text(hostname_xpath, self.host)
        self.browser.input_text(port_xpath, str(self.port))
        self.browser.input_text(username_xpath, "user-" + self.user)
        self.browser.input_text(password_xpath, self.password)
        self.browser.click_element_when_visible(save_changes_xpath)

        try:
            self.browser.go_to(url1)
            self.browser.wait_until_element_is_visible(connect_button_xpath, timeout=120)
            self.browser.click_element_when_visible(connect_button_xpath)
            self.browser.wait_until_element_is_visible(disconnect_button_xpath, timeout=120)
        except Exception as ex:
            if self.browser.does_page_contain_element(connect_button_xpath):
                logger.exception("Extension was not able to connect to the proxy.")
                raise ExtensionNotConnectedException("Extension was not able to connect to the proxy")
            else:
                logger.exception(ex)
                raise ex

    def test_connection(self):
        """Verify proxy connection by comparing IP addresses.

        Compares current IP address with the initial IP to confirm proxy is working.

        Returns:
            bool: True if proxy connection is verified

        Raises:
            IPAddressValidationException: If current IP matches initial IP,
                indicating proxy connection failure
        """
        logger.debug("Testing proxy connection...")
        ip = self.__get_current_ip()
        if ip != self.initial_ip:
            logger.debug(f"Proxy connection is working. IP: {ip}")
        else:
            logger.exception(f"Proxy connection is not working. IP: {ip}")
            raise IPAddressValidationException("Proxy connection is not working.")
        return True
