
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from app import app, db, load_user

class SearchTest(unittest.TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        #self.browser = webdriver.Edge()
        self.browser = webdriver.Chrome()
        self.browser.get('http://localhost:5000/')
    
    def testSucessfulSearch(self):
        #Signing up the test user
        #usename = test, password = 1 
        existing_user = load_user('test')
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

            submit = self.browser.find_element(By.ID, 'submit')
            submit.click()

        #Sighing in the test user
        id = self.browser.find_element(By.ID, 'id')
        self.assertIsNotNone(id)
        id.send_keys('test')

        password = self.browser.find_element(By.ID, 'password')
        self.assertIsNotNone(password)
        password.send_keys('test')

        submit = self.browser.find_element(By.ID, 'submit')
        submit.click()

        #Test Search Functionality 
        search = self.browser.find_element(By.ID, 'id')


        #page = self.browser.current_url
        #self.assertEqual('http://localhost:5000/index.html', page)