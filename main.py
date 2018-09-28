from selenium import webdriver
from bs4 import BeautifulSoup
from multiprocessing import process, Queue

class google_crawller(process):
    def __init__(self):
        super(google_crawller, self).__init__()

    def open_google(self, driver_path='./driver/chromedriver_window.exe'):
        driver = webdriver.Chrome(driver_path)
        driver.implicitly_wait(3)
        driver.get('https://google.com')
        return driver

    def search_term(self, driver, search_term):
        driver.find_element_by_id('lst-ib').send_keys('{} filetype:pdf'.format(search_term))
        driver.find_element_by_name('btnK').click()

    def get_result(self, driver)
        urls = []

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        for g in soup.find_all(class_='g'):
            print(g.cite.text)
            print('-----')
            url = g.cite.text
            urls.append(url)

        return urls

    def next_page(self, driver):
        driver.find_element_by_class_name('csb ch').click()