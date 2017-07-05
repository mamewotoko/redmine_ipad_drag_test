from unittest import TestLoader, TestSuite, TestCase
import unittest
import shutil
import itertools
import time
from HTMLTestRunner import HTMLTestRunner, HTMLTestCase
from ParametrizedTestCase import ParametrizedTestCase
import datetime
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

import os, re
import traceback
import urlparse

SCREENSHOT_DIR = "screenshot"

class WebTestCase(ParametrizedTestCase, HTMLTestCase):
    """ browse page and take screenshot
    """

    def setUp(self):
        user_agent, dim = self.param['user_agent']
        if len(user_agent) > 0:
            opts = Options()
            opts.add_argument("user-agent="+user_agent)
            self.driver = webdriver.Chrome(chrome_options=opts)
            self.driver.set_window_size(dim[0], dim[1])
        else:
            self.driver = webdriver.Chrome()
            
        self.screenshot = []

    def tearDown(self):
        self.driver.close()

    def save_screenshot(self, filename):
        path = "%s/%d_%s" % (SCREENSHOT_DIR, int(time.time()), filename)
        self.driver.save_screenshot(path)
        self.screenshot.append(path)

    def desc_html(self):
        return "<br/>" + str(self.param)

    def result_html(self):
        if not hasattr(self, 'screenshot'):
            return "no screenshot"

        img = ""
        for screen in self.screenshot:
            img += """ <div><img src="%s" /></div> """ % screen
        return img

class TopBottomWebTestCase(WebTestCase):
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
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.save_screenshot(screenshot_file+"_bottom.png")

if __name__ == "__main__":

    filename = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_report.html")
    
    params = {
        "url": [
            #"http://www.google.co.jp", 
            "http://www.asahi.com"
        ],
        "user_agent": [
            ("", None),
            ("Mozilla/5.0 (Linux; Android 4.1.2; SHL21 Build/S4011) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.83 Mobile Safari/537.36", (400, 600))
        ]
    }

    try:
        if os.path.exists(SCREENSHOT_DIR):
            shutil.rmtree(SCREENSHOT_DIR)
        os.makedirs(SCREENSHOT_DIR)
        with open(filename, "wb") as output:
            loader = TestLoader()
            suite = TestSuite()
            for (url, user_agent) in itertools.product(params["url"], params["user_agent"]):
                suite.addTest(ParametrizedTestCase.parametrize(TopBottomWebTestCase, param={"url": url, "user_agent": user_agent}))
            runner = HTMLTestRunner(stream = output, verbosity = 1, title="WebTest", show_mode=HTMLTestRunner.SHOW_ALL)
            runner.run(suite)
            print filename
    except:
        print(traceback.format_exc())
        if os.path.exists(filename):
            os.remove(filename)
