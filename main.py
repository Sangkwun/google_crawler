import os
import time
import urllib.request

from selenium import webdriver
from bs4 import BeautifulSoup
from multiprocessing import Process, Queue
from selenium.common.exceptions import NoSuchElementException
from urllib import parse


class Google_crawller(Process):
    def __init__(self, term_queue, pdf_url_queue, os):

        super(Google_crawller, self).__init__()  
        self._term_queue = term_queue
        self._pdf_url_queue = pdf_url_queue

        self._next = False
        self._open_chrome(os)
        self._duration = 15

        while self._driver is None:
            time.sleep(3)

    def _open_chrome(self, os):
        if os == "window":
            _driver_path = "./driver/chromedriver_window.exe"
        elif os == "mac":
            _driver_path = "./driver/chromedriver_mac"
        else:
            _driver_path = "./driver/chromedriver_linux"

        driver = webdriver.Chrome(_driver_path)
        driver.implicitly_wait(3)
        self._driver = driver

    def _search_term(self, search_term):
        self._driver.get('https://google.com/search?num=100&start=1&q={}'.format(search_term))

    def _get_result(self):

        html = self._driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        for g in soup.find_all(class_='g'):
            url = g.a['href']
            self._pdf_url_queue.put(url)

    def _chk_nex_page(self):
        try:
            self._driver.find_element_by_id('pnnext')
            return True
        except NoSuchElementException:
            return False

    def _next_page(self):

        self._driver.find_element_by_id('pnnext').click()
        time.sleep(self._duration)

    def run(self):
        while not self._term_queue.empty():
            try:
                term = self._term_queue.get()
                self._search_term(term)
                _next = self._chk_nex_page()

                while _next:
                
                    self._get_result()
                    self._next_page()
                    _next = self._chk_nex_page()
                    time.sleep(1)

            except Exception as err:
                print(err)


class Downloader(Process):
    def __init__(self, pdf_url_queue, directory):
        super(Downloader, self).__init__()
        self._pdf_url_queue = pdf_url_queue
        self._directory = directory

    def _validate_url(self, url):
        if url.startswith("http://") or url.startswith("https://"):
            return url
            
        return "https://{}".format(url)

    def run(self):
        while self._pdf_url_queue.empty():
            time.sleep(1)
        while not self._pdf_url_queue.empty():
            try:
                url = self._pdf_url_queue.get()
                last = url.split('/')[-1]
                filename = parse.unquote(last.split('.')[0]) +'.pdf'
                full_path = self._directory + '/' + filename
                url = self._validate_url(url)
                print(url, full_path)
                
                if not os.path.exists(full_path):
                    urllib.request.urlretrieve(url, full_path)
            except Exception as err:
                print(err)

def download(term_list, os="mac", directory="./pdf", num_crawller=2, num_downloader=4):
    term_queue = Queue()
    pdf_url_queue = Queue()
    [term_queue.put(term) for term in term_list]

    downloaders = [Downloader(pdf_url_queue=pdf_url_queue, directory=directory) for i in range(num_downloader)]
    crawllers = [Google_crawller(term_queue=term_queue, pdf_url_queue=pdf_url_queue, os=os) for i in range(num_crawller)]

    for crawller in crawllers:
        crawller.start()

    for downloader in downloaders:
        downloader.start()


if __name__ == '__main__':
    download(["검색어1", "검색어12", "3", "4", "5"])