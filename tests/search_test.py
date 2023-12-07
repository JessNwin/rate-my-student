#This first block of code prevents python module errors by adding the project root to the path environmental variable
#I kept getting errors so hopefully this solves them universally
import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)


import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from app import app, db
from app.models import User
from app import makeTestUsers 

class SearchTest(unittest.TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.browser = webdriver.Chrome() #WARNING: Chrome is made for the tests, so it must be installed
        self.browser.get('http://localhost:5000/')

    def testSucessfulSearch(self):
        #Test user: usename = test, password = 1 
        with app.app_context():
            query = User.query.filter_by(id='test').first()
            if query is None:
                makeTestUsers.makeTestUser()
            
            #Signin the test user
            signinButton = self.browser.find_elements(By.TAG_NAME, 'button')[1]
            wait = WebDriverWait(self.browser, 2)
            signinButton = wait.until(expected_conditions.element_to_be_clickable(signinButton))
            signinButton.click()
            
            id = self.browser.find_element(By.ID, 'id')
            id = wait.until(expected_conditions.presence_of_element_located((By.ID, 'id')))
            self.assertIsNotNone(id)
            id.send_keys('test')     

            password = self.browser.find_element(By.ID, 'password')
            password = wait.until(expected_conditions.presence_of_element_located((By.ID, 'password')))
            self.assertIsNotNone(password)
            password.send_keys('1')

            submit = self.browser.find_element(By.XPATH, '//input[@type="submit"]') 
            submit = wait.until(expected_conditions.presence_of_element_located((By.XPATH, '//input[@type="submit"]')))
            submit.click()

            #Test Search Functionality 
            search = self.browser.find_element(By.ID, 'search-input')
            search = wait.until(expected_conditions.presence_of_element_located((By.ID, 'search-input')))
            self.assertIsNotNone(search)
            search.send_keys('test')

            # waits for 10 seconds so the search suggestion has time to appear
            first_suggestion = wait.until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, '#suggestions-container div')))
            first_suggestion = self.browser.find_element(By.CSS_SELECTOR, '#suggestions-container div')
            first_suggestion.click()
            
            page = self.browser.current_url
            self.assertEqual('http://localhost:5000/users/test', page)
            removeTestUser = User.query.filter_by(id='test').first()
            db.session.delete(removeTestUser)
            db.session.commit()
            
if __name__ == '__main__':
    unittest.main()   