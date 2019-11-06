from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from sys import platform as _platform
import abc
import os

if _platform == 'linux' or _platform == 'linux2':
    drv_eng = 'web_driver/linux/chromedriver'
elif _platform == 'win32':
    drv_eng = 'web_driver/windows/chromedriver.exe'
elif _platform == 'darwin':
    drv_eng = 'web_driver/osx/chromedriver'

if not os.path.exists(drv_eng):
    chrome_driver_url = 'https://sites.google.com/a/chromium.org/chromedriver/downloads'
    raise FileNotFoundError(f'Web_driver not found - {drv_eng}, please goto {chrome_driver_url}')


class LinkCollector(metaclass=abc.ABCMeta):
    def __init__(self, url, headless=True):
        opt = Options()
        if headless:
            opt.add_argument('--headless')
            opt.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(drv_eng, options=opt)
        self.__links = []
        self.__next_page = None
        self.__load_page(url)
        self.process()

    def __load_page(self, url):
        print(f'Processing {url} ...')
        self.driver.get(url)

    def __process_next_page(self):
        self.__next_page = self.get_next_page()
        if not self.__next_page:
            return

        def routine_job():
            self.__load_page(self.__next_page)
            self.__links.extend(self.get_links_the_page())
            self.__next_page = self.get_next_page()

        while True:
            reply = input('Found next page, continue? [Yes/No/Auto]')
            if reply[0].lower() not in ['y', 'n', 'a']:
                continue

            if reply[0].lower() == 'a':
                while True:
                    try:
                        routine_job()
                        if not self.__next_page:
                            return
                    except KeyboardInterrupt:
                        return
            elif reply[0].lower() == 'y':
                routine_job()
                if not self.__next_page:
                    return
                continue
            else:
                return

    def process(self):
        self.__links.extend(self.get_links_the_page())
        self.__process_next_page()

    def dump(self):
        for idx, link in enumerate(self.__links, start=1):
            print(f'{idx}. {link}')

    @abc.abstractmethod
    def get_links_the_page(self):
        pass

    @abc.abstractmethod
    def get_next_page(self):
        pass
