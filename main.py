import urllib3

from selenium import webdriver
from bs4 import BeautifulSoup
from multiprocessing import Process, Queue
from selenium.common.exceptions import NoSuchElementException


class Google_crawller(Process):
    def __init__(self, term_queue, pdf_url_queue, os="window"):

        super(Google_crawller, self).__init__()  
        self._term_queue = term_queue
        self._pdf_url_queue = pdf_url_queue

        self._driver_path = ""
        self._next = False
        
        if os == "windor":
            self._driver_path = "./driver/chromedriver_window.exe"
        elif os == "mac":
            self._driver_path = "./driver/chromedriver_mac"
        else:
            self._driver_path = "./driver/chromedriver_linux"

        self._driver = self._open_chrome()

    def _open_chrome(self):
        driver = webdriver.Chrome(self._driver_path)
        driver.implicitly_wait(3)
        driver.get('https://google.com')
        self._driver = driver
    
    def _return_home(self):
        self._driver.get('https://google.com')

    def _search_term(self, search_term):
        self._driver.find_element_by_id('lst-ib').send_keys('{} filetype:pdf'.format(search_term))
        self._driver.find_element_by_name('btnK').click()

    def _get_result(self, driver):
        urls = []

        html = self._driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        for g in soup.find_all(class_='g'):
            url = g.cite.text
            urls.append(url)

        return urls

    def _next_page(self, driver):
        try:
            self._driver.find_element_by_class_name('csb ch').click()

        except NoSuchElementException:
            self._next = False

    def run(self):
        while self._image_queue.empty() == False:
            try:
                self._next = True
                self._return_home()
                term = self._queue.get()
                self._search_term(term)

                while self._next:
                
                    urls = self._get_result()
                    [self._pdf_url_queue.put(url) for url in urls]

                    self._next_page()

            except err:
                print(err)

#class Downloader(Process):


def download(term, os="window"):


if __name__ == '__main__':
    pass