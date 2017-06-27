from unittest import TestLoader, TestSuite, TestCase
import unittest
from HTMLTestRunner import HTMLTestRunner
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os, re
import traceback
import urlparse

SCREENSHOT_DIR = "screenshot"

# http://eli.thegreenplace.net/2011/08/02/python-unit-testing-parametrized-test-cases
class ParametrizedTestCase(unittest.TestCase):
    """ TestCase classes that want to be parametrized should
        inherit from this class.
    """
    def __init__(self, methodName='runTest', param=None):
        super(ParametrizedTestCase, self).__init__(methodName)
        self.param = param

    @staticmethod
    def parametrize(testcase_klass, param=None):
        """ Create a suite containing all tests taken from the given
            subclass, passing them the parameter 'param'.
        """
        testloader = unittest.TestLoader()
        testnames = testloader.getTestCaseNames(testcase_klass)
        suite = unittest.TestSuite()
        for name in testnames:
            suite.addTest(testcase_klass(name, param=param))
        return suite

class PythonTest(ParametrizedTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.close()

    def test_site(self):
        driver = self.driver
        url = self.param['url']
        urlobj = urlparse.urlparse(url)
        screenshot_file = urlobj.hostname + re.sub(r"[/:%]", "_", urlobj.path)
        driver.get(url)
        driver.save_screenshot(screenshot_file+".png")

if __name__ == "__main__":

    filename = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_report.html")
    urllist = [
        "http://www.google.co.jp", 
        "http://www.asahi.com"
    ]

    try:
        if os.path.exists(SCREENSHOT_DIR):
            os.removedirs(SCREENSHOT_DIR)
        os.makedirs(SCREENSHOT_DIR)
        with open(filename, "wb") as output:
            loader = TestLoader()
            suite = TestSuite()
            for url in urllist:
                suite.addTest(ParametrizedTestCase.parametrize(PythonTest, param={"url": url}))
            runner = HTMLTestRunner(stream = output, verbosity = 1, title="WebTest")
            runner.run(suite)
            print filename
    except:
        print(traceback.format_exc())
        if os.path.exists(filename):
            os.remove(filename)
