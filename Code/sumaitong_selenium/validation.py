import selenium
from selenium import webdriver

class Validation():
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(20)
