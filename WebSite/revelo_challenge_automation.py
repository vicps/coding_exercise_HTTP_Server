import unittest , subprocess, time, os, csv, requests, concurrent.futures
from selenium import webdriver
from selenium.webdriver.common.by import By
from revelo_challenge_automation_page import URLShortenerPage
from time import sleep

class URLShortenerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Start the Flask server
        cls.server = subprocess.Popen(['python', 'revelo_challenge.py'])
        sleep(3)

    @classmethod
    def tearDownClass(cls):
        # Terminate the Flask server after all tests have run
        cls.server.terminate()

   
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.page = URLShortenerPage(self.driver)
        self.page.open()

    #test cases for positive scenarios

    def test_url_shortening(self):
        original_url = "https://www.uol.com.br/"
        self.page.shorten_url(original_url)
        sleep(1)
        short_url = self.page.get_shortened_url()
        sleep(1)
        self.assertIn("http://127.0.0.1:5000/", short_url)

    def test_url_retrieval(self):
        original_url = "https://www.uol.com.br/"
        self.page.shorten_url(original_url)
        sleep(1)
        short_url = self.page.get_shortened_url()
        sleep(1)
        self.page.retrieve_url(short_url)
        sleep(1)
        retrieved_url = self.page.get_retrieved_url()
        self.assertIn(original_url, retrieved_url)

    def test_url_counting_zero(self):
        original_url = "https://www.uol.com.br/"
        self.page.shorten_url(original_url)
        sleep(1)
        short_url = self.page.get_shortened_url()
        self.page.count_url(short_url)
        sleep(1)
        count_clicks = self.page.get_count_url()
        self.assertEqual(count_clicks, "How many times this shortened URL was clicked: 0")

    def test_url_counting_multiple(self):
        original_url = "https://www.uol.com.br/"
        self.page.shorten_url(original_url)
        sleep(1)
        short_url = self.page.get_shortened_url()
        # Remove the "Shortened URL: " part of the string
        short_url = short_url.replace("Shortened URL: ", "")        
        # Open a new tab and use the shortened URL
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.get(short_url)
        sleep(1)        
        # Switch back to the original tab
        #self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
        # Check the URL count
        self.page.count_url(short_url)
        sleep(1)
        count_clicks = self.page.get_count_url()
        self.assertEqual(count_clicks, "How many times this shortened URL was clicked: 1")
    
    #testing the logs
    def test_log_content(self):
        # Check if log file exists
        log_file = 'revelo_challenge_logs.csv'
        self.assertTrue(os.path.exists(log_file))
        
        # Read the CSV log file content
        with open(log_file, 'r') as file:
            reader = csv.reader(file)
            rows = list(reader)
        
        # Flatten the list of log messages to ensure all messages are checked
        messages = [row[2] for row in rows if len(row) > 2]
        
        # Check if specific log messages are present
        self.assertIn("Starting Flask application.", messages)
        self.assertIn("Received URL to shorten: https://www.uol.com.br/", messages)



    #test cases for negative scenarios

    def test_invalid_url_input_shortening(self):
        
        invalid_url = "invalid-url"
        sleep(1)
        self.page.shorten_url(invalid_url)
        sleep(1)
        error_message = self.page.get_error_message()
        sleep(1)
        self.assertIn("Error: Invalid URL", error_message)

    def test_empty_url_input_shortening(self):                
        self.page.shorten_url("")
        sleep(1)
        error_message = self.page.get_error_message()
        self.assertIn("Error: Invalid URL", error_message)

    def test_notDuplicate_url_shortening(self):        
        original_url = "https://www.uol.com.br/"
        self.page.shorten_url(original_url)
        sleep(1)
        first_short_url = self.page.get_shortened_url()
        sleep(1)
        self.page.shorten_url(original_url)
        sleep(1)
        second_short_url = self.page.get_shortened_url()
        sleep(1)
        self.assertEqual(first_short_url, second_short_url)

    def test_invalid_url_input_retrieving(self):        
        invalid_url = "invalid-url"
        sleep(1)
        self.page.retrieve_url(invalid_url)
        sleep(1)
        error_message = self.page.get_error_message_retrieve()
        sleep(1)
        self.assertIn("Error: Short URL not found", error_message)

    def test_empty_url_input_retrieving(self):                
        self.page.shorten_url("")
        sleep(1)
        error_message = self.page.get_error_message_retrieve()
        self.assertIn(error_message, "Error: Short URL not found")

    def test_invalid_url_input_counting(self):        
        invalid_url = "invalid-url"
        sleep(1)
        self.page.count_url(invalid_url)
        sleep(1)
        error_message = self.page.get_error_message_count()
        sleep(1)
        self.assertIn("Error: Short URL not found", error_message)

    #testing concurrent requests while shortening a url
    def test_concurrent_url_shortening(self):
        original_url = "https://www.uol.com.br/"
        num_requests = 10  # Number of concurrent requests

        def shorten_url():
            response = requests.post('http://127.0.0.1:5000/shorten', data={'original_url': original_url})
            return response

        with concurrent.futures.ThreadPoolExecutor(max_workers=num_requests) as executor:
            futures = [executor.submit(shorten_url) for _ in range(num_requests)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]

        # Check that all requests were successful
        for result in results:
            self.assertEqual(result.status_code, 200)
            self.assertIn('short_url', result.json())

  

    #closing the browser
    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
