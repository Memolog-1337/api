import random

from selenium.webdriver import Chrome, ChromeOptions
from selenium_stealth import stealth
from bs4 import BeautifulSoup


MOUSER_URL: str = 'https://www.mouser.com'
QUEST_URL: str = 'https://www.mouser.com/c/?q='
PROXY_LIST: list = [
    '196.19.176.231:8000',
    '196.17.250.47:8000',
    '45.147.103.118:8000',
]
PATH_TO_CHROMEDRIVER: str = ('D:\\Ycheba\\PythonED\\'
                             'Chromedriver\\chromedriver.exe')


class StealthBrowser:
    proxy: str
    options = ChromeOptions()  # нужен typing

    def __init__(self) -> None:
        self.proxy: str = random.choice(PROXY_LIST)
        # Разобраться в этих настройках
        self.options.add_argument('--proxy-server=%s' % self.proxy)
        self.options.add_argument('--profile-directory=Profile 1')
        self.options.add_experimental_option(
            'excludeSwitches',
            ['enable-automation']
        )
        # self.options.add_argument('--headless')
        self.options.add_experimental_option('useAutomationExtension', False)
        self.browser = Chrome(
            executable_path=PATH_TO_CHROMEDRIVER,
            options=self.options
        )  # Вынести параметр в объявление класса и сделать tuping
        stealth(
            self.browser,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True
        )

    def get_url(self, url):  # typing
        self.browser.get(url)

    def get_soup_info(self):  # typing
        return BeautifulSoup(self.browser.page_source, 'lxml')
