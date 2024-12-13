import json
import time

from selenium.webdriver.chrome.options import Options

from t_proxy.browser.t_proxy_core import BrowserProxyCore
from t_proxy.config import CONFIG
from t_proxy.exceptions import ExtensionEmptyUUIDException, ExtensionInstallException
from t_proxy.utils.logger import logger


class ProxyChrome(BrowserProxyCore):
    """Chrome browser proxy implementation.

    This class manages Chrome browser proxy configuration, including extension installation,
    authentication, and connection testing.

    Inherits from BrowserProxyCore.
    """

    def __init__(self, user: str, password: str, port: int, host: str, options: Options):
        """Initialize Chrome proxy configuration.

        Args:
            user (str): Proxy username for authentication
            password (str): Proxy password for authentication
            port (int): Proxy port number
            host (str): Proxy host address
            options (Options): Chrome browser options. If None, default Options() will be used
        """
        super().__init__(user, password, port, host)
        self.options = options if options else Options()

    def start(self):
        """Initialize and configure the Chrome proxy connection.

        Performs the following steps:
        1. Installs the Oxylabs extension
        2. Generates extension URLs using the obtained UUID
        3. Authenticates with the extension
        4. Verifies the proxy connection

        Raises:
            ExtensionInstallException: If extension installation fails
            ExtensionEmptyUUIDException: If unable to obtain extension UUID
        """
        self.install_extension()
        url1 = self.chrome_extension_url.format(self.uuid)
        url2 = self.chrome_extension_url_options.format(self.uuid)
        self.login_on_chrome_extension(url1, url2)
        self.test_connection()

    def install_extension(self):
        """Install the Oxylabs extension in Chrome browser.

        Adds the extension to Chrome options and initializes the browser with specified
        user agent and options. Includes a 5-second delay to ensure proper extension loading.

        Raises:
            ExtensionInstallException: If the extension installation fails for any reason
        """
        logger.debug("Installing Oxylabs extension...")
        try:
            self.options.add_extension(CONFIG.PATHS.CHROME_EXTENSION_PATH)
            self.browser.open_available_browser(
                user_agent=self.user_agent.chrome, browser_selection="chrome", options=self.options
            )
            self.obtain_extension_uuid()
            time.sleep(5)

        except Exception as ex:
            logger.exception(ex)
            raise ExtensionInstallException("Module failed to install Oxylabs extension")

    def obtain_extension_uuid(self):
        """Retrieve the installed Oxylabs extension UUID.

        Navigates to Chrome's internal extensions page and parses the JSON data
        to find the Oxylabs extension ID.

        Raises:
            ExtensionEmptyUUIDException: If unable to find the Oxylabs extension UUID

        Sets:
            self.uuid: The extension UUID string
        """
        logger.debug("Getting extension uuid...")
        self.browser.go_to("chrome://extensions-internals/")
        internals_json = self.browser.get_webelement("//pre").text
        internals = json.loads(internals_json)
        for extension in internals:
            if "Oxylabs" in extension.get("name", ""):
                self.uuid = extension["id"]
                break
        else:
            raise ExtensionEmptyUUIDException("Module failed to get installed extension uuid")
        logger.debug(f"Extension uuid is: {self.uuid}")
