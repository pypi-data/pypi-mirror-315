import json
import time

import requests

from t_proxy.browser.t_proxy_core import BrowserProxyCore
from t_proxy.config import CONFIG
from t_proxy.exceptions import (
    EnablePrivateBrowsingException,
    ExtensionDownloadException,
    ExtensionEmptyUUIDException,
    ExtensionInstallException,
)
from t_proxy.utils.logger import logger


class ProxyFirefox(BrowserProxyCore):
    """Firefox browser proxy implementation.

    This class manages Firefox browser proxy configuration, including extension installation,
    authentication, and connection testing.

    Inherits from BrowserProxyCore.
    """

    def __init__(self, user: str, password: str, port: int, host: str, options: dict):
        """Initialize Firefox proxy configuration.

        Args:
            user (str): Proxy username for authentication
            password (str): Proxy password for authentication
            port (int): Proxy port number
            host (str): Proxy host address
            options (dict): Firefox browser preferences/options
        """
        super().__init__(user, password, port, host)
        self.options = options

    def start(self):
        """Initialize and configure the Firefox proxy connection.

        Performs the following steps:
        1. Opens the Firefox browser
        2. Installs the Oxylabs extension
        3. Obtains the extension UUID
        4. Authenticates with the extension
        5. Verifies the proxy connection

        Raises:
            ExtensionInstallException: If extension installation fails
            ExtensionEmptyUUIDException: If unable to obtain extension UUID
            EnablePrivateBrowsingException: If private browsing setup fails
        """
        # self.__download_extension()
        self.open_browser()
        self.install_extension()
        self.obtain_extension_uuid()
        url1 = self.firefox_extension_url.format(self.uuid)
        url2 = self.firefox_extension_url_options.format(self.uuid)
        self.login_on_firefox_extension(url1, url2)
        self.test_connection()

    def open_browser(self):
        """Initialize and open Firefox browser instance.

        Opens Firefox with specified user agent and preferences.

        Raises:
            Exception: If browser fails to open with detailed error message
        """
        try:
            logger.debug("Opening Firefox browser...")
            self.browser.open_available_browser(
                user_agent=self.user_agent.firefox, preferences=self.options, browser_selection="firefox"
            )
        except Exception as ex:
            logger.exception(ex)
            raise Exception(f"Module failed to open Firefox browser: {ex}")

    def __download_extension(self):
        """Download the Oxylabs extension from configured URL.

        Downloads and saves the extension file to the configured path.

        Raises:
            ExtensionDownloadException: If extension download fails
        """
        logger.debug("Downloading Oxylabs extension...")
        try:
            response = requests.get(CONFIG.URLS.FIREFOX_EXTENSION_URL)
            with open(CONFIG.PATHS.FIREFOX_EXTENSION_PATH, mode="wb") as f:
                f.write(response.content)
            logger.debug("Oxylabs extension downloaded successfully")
        except Exception as ex:
            logger.exception(ex)
            raise ExtensionDownloadException("Module failed to download Oxylabs extension")

    def install_extension(self):
        """Install the Oxylabs extension in Firefox browser.

        Installs the extension and configures private browsing access.
        Includes a 5-second delay to ensure proper extension loading.

        Raises:
            ExtensionInstallException: If extension installation fails
        """
        logger.debug("Installing Oxylabs extension...")
        try:
            self.id = self.browser.driver.install_addon(CONFIG.PATHS.FIREFOX_EXTENSION_PATH)
            time.sleep(5)
            self.allow_private_browsing_ui()
        except Exception as ex:
            logger.exception(ex)
            raise ExtensionInstallException("Module failed to install Oxylabs extension")

    def obtain_extension_uuid(self):
        """Retrieve the installed Oxylabs extension UUID.

        Reads Firefox profile preferences to find the extension UUID.

        Raises:
            ExtensionEmptyUUIDException: If unable to find the extension UUID

        Sets:
            self.uuid: The extension UUID string
        """
        logger.debug("Getting extension uuid...")
        profile_path = self.browser.driver.capabilities["moz:profile"]
        with open("{}/prefs.js".format(profile_path), "r") as file_prefs:
            lines = file_prefs.readlines()
            for line in lines:
                if "extensions.webextensions.uuids" in line:
                    extensions = json.loads(line[45:-4].replace("\\", ""))
                    if self.id in extensions:
                        self.uuid = extensions[self.id]
                        break
        if self.uuid == "":
            raise ExtensionEmptyUUIDException("Module failed to get installed extension uuid")
        logger.debug(f"Extension uuid is: {self.uuid}")

    def allow_private_browsing_ui(self):
        """Enable private browsing access for the Oxylabs extension.

        Navigates through Firefox UI to enable private browsing access for the extension.
        Required for VPN/Proxy functionality.

        Raises:
            EnablePrivateBrowsingException: If unable to enable private browsing access
        """
        logger.debug("Enabling extension private browsing...")
        self.browser.go_to("about:addons")
        self.browser.wait_until_element_is_visible('//button[@title="Extensions"]')
        self.browser.click_button_when_visible('//button[@title="Extensions"]')
        clicked = False
        for _ in range(0, 10):
            try:
                self.browser.execute_javascript(f"document.querySelector('[addon-id=\"{self.id}\"]').click()")
                self.browser.execute_javascript('document.getElementsByName("private-browsing")[0].click()')
                clicked = True
                break
            except Exception as ex:
                logger.exception(ex)
        self.browser.wait_until_element_is_visible('//button[@title="Extensions"]')
        self.browser.click_button_when_visible('//button[@title="Extensions"]')
        if not clicked:
            raise EnablePrivateBrowsingException("Failed to enable private browsing")
