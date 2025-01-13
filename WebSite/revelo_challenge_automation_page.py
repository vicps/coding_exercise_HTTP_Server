from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from time import sleep



class URLShortenerPage:

    #basic driver initialization
    def __init__(self, driver):
        self.driver = driver
        self.url = "http://127.0.0.1:5000"

    #buttons
        self.shorten_button = (By.XPATH, "/html/body/form[1]/input[2]")
        self.retrieve_button = (By.XPATH, "/html/body/form[2]/input[2]")
        self.count_button = (By.XPATH, "/html/body/form[3]/input[2]")


    #text boxes for inputs
        self.original_url_input = (By.ID, "original_url")
        self.shortened_url_input = (By.ID, "shorten_url")
        self.count_url_input = (By.ID, "count_url")


    #results and error messages texts    
        
        self.shortened_url_text = (By.ID, "shorten-result")             
        self.retrieved_url_text = (By.ID, "retrieve-result")
        self.count_url_text = (By.ID, "count-result")


    #METHODS

    

    def open(self):
        self.driver.get(self.url)

    #inputs

    def shorten_url(self, original_url):
        #cleaning any possible previous input
        self.driver.find_element(*self.original_url_input).clear()        
        self.driver.find_element(*self.original_url_input).send_keys(original_url)
        self.driver.find_element(*self.shorten_button).click()

    def retrieve_url(self, short_url):
        #cleaning any possible previous input
        self.driver.find_element(*self.shortened_url_input).clear()
        self.driver.find_element(*self.shortened_url_input).send_keys(short_url)
        self.driver.find_element(*self.retrieve_button).click()

    def count_url(self,short_url):
        #cleaning any possible previous input
        self.driver.find_element(*self.count_url_input).clear()
        self.driver.find_element(*self.count_url_input).send_keys(short_url)
        self.driver.find_element(*self.count_button).click()
        
    #get results

    def get_shortened_url(self):
        return self.driver.find_element(*self.shortened_url_text).text

    def get_retrieved_url(self):
        return self.driver.find_element(*self.retrieved_url_text).text

    def get_count_url(self):            
        return self.driver.find_element(*self.count_url_text).text

    def get_error_message(self):
        return self.driver.find_element(*self.shortened_url_text).text
    
    def get_error_message_retrieve(self):
        return self.driver.find_element(*self.retrieved_url_text).text
    
    def get_error_message_count(self):
        return self.driver.find_element(*self.count_url_text).text