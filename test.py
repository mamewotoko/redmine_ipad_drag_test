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
            img += """ <div><img class="screenshot" src="%s" /></div> """ % screen
        return img

class TopBottomWebTestCase(WebTestCase):
    def login_and_open_backlog(self):
        driver = self.driver
        url = 'http://localhost:3001/redmine/'
        urlobj = urlparse.urlparse(url)
        screenshot_file = urlobj.hostname + re.sub(r"[/:%]", "_", urlobj.path)
        driver.get(url)
        login_link = driver.find_element_by_xpath('//*[@id="account"]/ul/li[1]/a')
        login_link.click()
        username_text = driver.find_element_by_xpath('//*[@id="username"]')
        username_text.send_keys('admin')
        password_text = driver.find_element_by_xpath('//*[@id="password"]')
        password_text.send_keys('admin')
        login_button = driver.find_element_by_xpath('//*[@id="login-form"]/form/table/tbody/tr[4]/td[2]/input')
        login_button.click()

        body = driver.find_element_by_xpath("//body")
        self.save_screenshot(screenshot_file+".png")

        # project test
        driver.find_element_by_xpath('//*[@id="content"]/div[2]/div/ul/li/a').click()
        time.sleep(1)
        self.save_screenshot(screenshot_file+"1.png")

        # backlog
        driver.find_element_by_xpath('//*[@id="main-menu"]/ul/li[4]/a').click()
        time.sleep(1)
        self.save_screenshot(screenshot_file+"2.png")

    def test_backlog():
        self.login_and_open_backlog()
        
    def test_dragging_story(self):
        driver = self.driver
        url = 'http://localhost:3001/redmine/rb/taskboards/1'

        urlobj = urlparse.urlparse(url)
        screenshot_file = urlobj.hostname + re.sub(r"[/:%]", "_", urlobj.path)

        self.login_and_open_backlog()
        
        story = driver.find_element_by_xpath('//*[@id="story_1"]/div[1]/div')
        #target = driver.find_element_by_xpath('//*[@id="stories-for-1"]')
        target = driver.find_element_by_xpath('//*[@id="stories-for-2"]')
        self.save_screenshot(screenshot_file+"2.png")

        ActionChains(driver).click_and_hold(story).move_to_element(target).release(target).perform()
        time.sleep(1)
        
        self.save_screenshot(screenshot_file+"3.png")
        ## TODO: add assert

    def test_dragging_task(self):
        self.login_and_open_backlog()
        
        url = 'http://localhost:3001/redmine/rb/taskboards/1'
        urlobj = urlparse.urlparse(url)
        screenshot_file = urlobj.hostname + re.sub(r"[/:%]", "_", urlobj.path)
        driver = self.driver

        kanban_link = driver.find_element_by_xpath('//*[@id="main-menu"]/ul/li[5]/a')
        kanban_link.click()
        time.sleep(1)

        task_add_button = driver.find_element_by_xpath('//*[@id="swimlane-2"]/td[1]/div/div[1]/span[1]/img')
        task_add_button.click()
        task_title = driver.find_element_by_xpath('//*[@id="task_editor"]/textarea')
        task_title.send_keys('task title')
        ok_button = driver.find_element_by_xpath('//button/span[text()="OK"]')

        ok_button.click()
        self.save_screenshot(screenshot_file+".png")
        ## TODO: add assert
        task = driver.find_element_by_xpath('//div[@id="issue_6"]')
        target = driver.find_element_by_xpath('//*[@id="2_5"]')
        ActionChains(driver).click_and_hold(task).move_to_element(target).release(target).perform()
        time.sleep(1)
        self.save_screenshot(screenshot_file+".png")
       
        
if __name__ == "__main__":

    filename = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_report.html")
    
    params = {
        "user_agent": [
            ("Mozilla/5.0 (Linux; Android 4.1.2; SHL21 Build/S4011) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.83 Mobile Safari/537.36", (1024, 800))
        ]
    }

    try:
        if os.path.exists(SCREENSHOT_DIR):
            shutil.rmtree(SCREENSHOT_DIR)
        os.makedirs(SCREENSHOT_DIR)
        with open(filename, "wb") as output:
            loader = TestLoader()
            suite = TestSuite()
            for user_agent in params["user_agent"]:
                suite.addTest(ParametrizedTestCase.parametrize(TopBottomWebTestCase, param={"user_agent": user_agent}))
            runner = HTMLTestRunner(stream = output, verbosity = 1, title="WebTest", show_mode=HTMLTestRunner.SHOW_ALL)
            runner.run(suite)
            print filename
    except:
        print(traceback.format_exc())
        if os.path.exists(filename):
            os.remove(filename)
