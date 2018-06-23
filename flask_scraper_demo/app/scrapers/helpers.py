import os
import random

# import shapefile
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


DEFAULT_WINDOW_SIZE = (1366, 768)
DEFAULT_LOG_PATH = os.path.devnull

USER_AGENTS = (
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0.2 Safari/604.4.7',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
)
"""
Tuple[str]: Set of user agents that we randomly choose from to seem "human".
    Source: https://techblog.willshouse.com/2012/01/03/most-common-user-agents/
"""


def init_chrome_webdriver(
        executable_path='chromedriver', download_dir=None,
        window_size=None, user_agent=None, log_path=None,
        headless=True, incognito=True,
        ignore_certificate_errors=True,
        disable_gpu=True, disable_notifications=True, disable_infobars=True):
    """
    Configure and initialize the ChromeDriver service, then create and return a
    new instance of the Chrome web driver, via ``selenium``.

    Args:
        executable_path (str): Path to ChromeDriver executable, downloadable from
            http://chromedriver.storage.googleapis.com/index.html. If 'chromedriver',
            the executable must be somewhere in ``$PATH``.
        window_size (Tuple[int, int]): Size (width x height) of browser window.
            If None, a default window size is used.
        user_agent (str): Set browser's user agent; If None, a common user agent
            is randomly selected. This can be useful for "spoofing".
        log_path (str): Path on disk to which logging statements are written.
            If None, '/dev/null' is used by default, effectively disabling logging.
        headless (bool): If True, run browser in headless mode, i.e. without a UI
            or display server dependencies; otherwise, open a regular browser window.
        incognito (bool): Launch browser in incognito mode.
        ignore_certificate_errors (bool): If True, ignore certificate-related
            errors; otherwise, raise exceptions for such errors.
        disable_gpu (bool): If True, disable GPU hardware acceleration; otherwise,
            attempt to use GPU when rendering.
        disable_notifications (bool): If True, disable web notification and push APIs.
        disable_infobars (bool): If True, prevent infobars from appearing.

    Returns:
        :class:`webdriver.Chrome()`

    References:
        A complete list of chrome options can be found here:
        https://peter.sh/experiments/chromium-command-line-switches/
    """
    options = webdriver.ChromeOptions()

    # set boolean switch args
    if headless is True:
        options.add_argument('--headless')
    if incognito is True:
        options.add_argument('--incognito')
    if ignore_certificate_errors is True:
        options.add_argument('--ignore-certificate-errors')
    if disable_gpu is True:
        options.add_argument('--disable-gpu')
    if disable_notifications is True:
        options.add_argument('--disable-notifications')
    if disable_infobars is True:
        options.add_argument('--disable-infobars')

    # Needed to run in docker
    options.add_argument('--no-sandbox')

    # set window size, using a global default if not specified
    # (does this matter if `headless=True`?)
    if not window_size:
        window_size = DEFAULT_WINDOW_SIZE
    options.add_argument('--window-size={w},{h}'.format(w=window_size[0], h=window_size[1]))

    # set user-agent, using a randomly selected default if not specified
    if not user_agent:
        user_agent = random.choice(USER_AGENTS)
    options.add_argument('--user-agent="{}"'.format(user_agent))

    # get a global default for logging path if not specified
    # value passed in webdriver.Chrome init
    if not log_path:
        log_path = DEFAULT_LOG_PATH

    capabilities = DesiredCapabilities.CHROME.copy()
    capabilities['version'] = 'latest'
    capabilities['loggingPref'] = {
        'driver': 'WARNING', 'server': 'WARNING', 'browser': 'WARNING'}

    prefs = {
        'profile.default_content_settings.popups': False,
        'directory_upgrade': True,
    }
    if download_dir:
        prefs['download.default_directory'] = download_dir
    options.add_experimental_option('prefs', prefs)

    # initialize the driver with specified configuration
    driver = webdriver.Chrome(
        executable_path=executable_path,
        options=options,
        desired_capabilities=capabilities,
        service_log_path=log_path)

    return driver


def randomized_sleep(duration):
    """
    Sleep a randomized amount of time between ``duration`` and 2 * ``duration`` seconds.
    """
    sleep(duration + duration * random.random())
