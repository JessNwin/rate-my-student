#This first block of code prevents python module errors by adding the project root to the path environmental variable
#I kept getting errors so hopefully this solves them universally
import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)


import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from app import app, db
from app.models import User

class SearchTest(unittest.TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.browser = webdriver.Chrome() #WARNING: Chrome is made for the tests, so it must be installed
        self.browser.get('http://localhost:5000/')

    def testSucessfulSearch(self):
        #Test user:usename = test, password = 1 

        with app.app_context():
            existing_user = db.session.query(User).filter_by(id='test').first()

            #If there is a test user already in the database, one is not created
            if existing_user != None:
                signinButton = self.browser.find_elements(By.TAG_NAME, 'button')[1]
                signinButton.click()

            #This creates a test user if there is not already one in the database
            if existing_user is None:
                signupButton = self.browser.find_elements(By.TAG_NAME, 'button')[0]
                signupButton.click()
                id = self.browser.find_element(By.ID, 'id')
                self.assertIsNotNone(id)
                id.send_keys('test')

                name = self.browser.find_element(By.ID, 'full_name')
                self.assertIsNotNone(name)
                name.send_keys('test')

                passwd = self.browser.find_element(By.ID, 'password')
                self.assertIsNotNone(passwd)
                passwd.send_keys('1')

                confirmPasswd = self.browser.find_element(By.ID, 'password_confirm')
                self.assertIsNotNone(confirmPasswd)
                confirmPasswd.send_keys('1')

                submit = self.browser.find_element(By.XPATH, '//input[@type="submit"]') 
                submit.click()

            #Signin the test user
            id = self.browser.find_element(By.ID, 'id')
            self.assertIsNotNone(id)
            id.send_keys('test')     

            password = self.browser.find_element(By.ID, 'password')
            self.assertIsNotNone(password)
            password.send_keys('1')

            submit = self.browser.find_element(By.XPATH, '//input[@type="submit"]') 
            submit.click()

            #Test Search Functionality 
            search = self.browser.find_element(By.ID, 'search-input')
            self.assertIsNotNone(search)
            search.send_keys('test')

            # waits for two seconds so the search suggestion has time to appear
            self.browser.implicitly_wait(2)

            first_suggestion = self.browser.find_element(By.CSS_SELECTOR, '#suggestions-container div')
            first_suggestion.click()

            page = self.browser.current_url
            self.assertEqual('http://localhost:5000/users/test', page)

if __name__ == '__main__':
    unittest.main()   