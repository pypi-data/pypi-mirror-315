from typing import Union

from selenium.webdriver.chrome.options import Options

from t_proxy.browser.chrome_proxy import ProxyChrome
from t_proxy.browser.firefox_proxy import ProxyFirefox
from t_proxy.requests.requests_proxy import ProxyRequests


class BrowserProxy:
    """Factory class for creating browser instances with proxy configuration.

    Provides methods to create Chrome or Firefox browsers with pre-configured
    proxy settings and authentication.
    """

    def chrome(
        self,
        user: str,
        password: str,
        port: int,
        host: str,
        options: Union[Options, None] = None,
    ):
        """Create and configure a Chrome browser with proxy settings.

        Args:
            user (str): Proxy username for authentication
            password (str): Proxy password for authentication
            port (int): Proxy port number
            host (str): Proxy host address
            options (Options, optional): Chrome-specific browser options. Defaults to None.

        Returns:
            webdriver.Chrome: Configured Chrome browser instance with active proxy connection
        """
        proxy_chrome = ProxyChrome(user, password, port, host, options)
        proxy_chrome.start()
        return proxy_chrome.browser

    def firefox(
        self,
        user: str,
        password: str,
        port: int,
        host: str,
        options: Union[dict, None] = None,
    ):
        """Create and configure a Firefox browser with proxy settings.

        Args:
            user (str): Proxy username for authentication
            password (str): Proxy password for authentication
            port (int): Proxy port number
            host (str): Proxy host address
            options (dict, optional): Firefox-specific browser options. Defaults to None.

        Returns:
            webdriver.Firefox: Configured Firefox browser instance with active proxy connection
        """
        proxy_firefox = ProxyFirefox(user, password, port, host, options)
        proxy_firefox.start()
        return proxy_firefox.browser


class RequestsProxy:
    """Factory class for creating requests sessions with proxy configuration.

    Provides methods to create requests sessions with pre-configured proxy
    settings and authentication.
    """

    def session(self, credentials: dict):
        """Create a requests session with proxy configuration.

        Args:
            credentials (dict): Dictionary containing proxy authentication details.
                Required keys: 'user', 'password', 'port', 'host'

        Returns:
            requests.Session: Configured session object with active proxy connection
        """
        proxy_requests = ProxyRequests(credentials)
        return proxy_requests.session
