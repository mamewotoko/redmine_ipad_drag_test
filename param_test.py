from unittest import TestLoader, TestSuite, TestCase
import unittest
from HTMLTestRunner import HTMLTestRunner, HTMLTestCase
from ParametrizedTestCase import ParametrizedTestCase
import datetime
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import os, re
import traceback
import urlparse

SCREENSHOT_DIR = "screenshot"

class WebTest(ParametrizedTestCase, HTMLTestCase):
    """ browse page and take screenshot
    """

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.screenshot = []

    def tearDown(self):
        self.driver.close()

    def save_screenshot(self, filename):
        path = SCREENSHOT_DIR+"/"+filename
        self.driver.save_screenshot(path)
        self.screenshot.append(path)

    def to_html(self):
        img = ""
        for screen in self.screenshot:
            img += """ <div><img src="%s" /></div> """ % screen
        return img

class TopBottomWebTest(WebTest):
    # sample
    def test_top(self):
        """ top of page
        """
        driver = self.driver
        url = self.param['url']
        urlobj = urlparse.urlparse(url)
        screenshot_file = urlobj.hostname + re.sub(r"[/:%]", "_", urlobj.path)
        driver.get(url)
        self.save_screenshot(screenshot_file+".png")

    # sample
    def test_bottom(self):
        """ bottom of page
        """
        driver = self.driver
        url = self.param['url']
        urlobj = urlparse.urlparse(url)
        screenshot_file = urlobj.hostname + re.sub(r"[/:%]", "_", urlobj.path)
        driver.get(url)
        ActionChains(driver).send_keys(Keys.CONTROL+Keys.END).perform()
        self.save_screenshot(screenshot_file+"_bottom.png")

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
                suite.addTest(ParametrizedTestCase.parametrize(TopBottomWebTest, param={"url": url}))
            runner = HTMLTestRunner(stream = output, verbosity = 1, title="WebTest", show_mode=HTMLTestRunner.SHOW_ALL)
            runner.run(suite)
            print filename
    except:
        print(traceback.format_exc())
        if os.path.exists(filename):
            os.remove(filename)
