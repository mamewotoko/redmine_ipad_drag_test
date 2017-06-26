from unittest import TestLoader, TestSuite, TestCase
import unittest
from HTMLTestRunner import HTMLTestRunner
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import traceback

class PythonTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.close()

    def test_site(self):
        driver = self.driver
        driver.get("http://www.python.org")
        driver.save_screenshot('screenshot0.png')

if __name__ == "__main__":

    filename = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_report.html")

    try:
        with open(filename, "wb") as output:
            loader = TestLoader()
            suite = TestSuite((loader.loadTestsFromTestCase(PythonTest)))
            #unittest.main()
            runner = HTMLTestRunner(stream = output, verbosity = 1, title="WebTest")
            runner.run(suite)
            print filename
    except:
        print(traceback.format_exc())
        os.remove(filename)
