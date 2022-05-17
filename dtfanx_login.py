from selenium import webdriver
import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "...", "..."))
#import HtmlTestRunner

class LoginPage(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print "seenu"
        cls.driver = webdriver.Firefox(executable_path="D:\Driver\geckodriver.exe")
        cls.driver.implicitly_wait(30)
        cls.driver.maximize_window()
        print "seenu"

    def test_01_user_aunthentication(self):
        driver = self.driver
        driver.get("https://demo-fanx.airislabs.com/app/")
        driver.find_element_by_xpath("/html/body/div/div/div/div[2]/input").send_keys("seenu@yopmail.com")
        driver.find_element_by_xpath("/html/body/div/div/div/div[3]/input").send_keys("Welco@20")
        driver.find_element_by_xpath("/html/body/div/div/div/div[4]/button").click()
        time.sleep(5)
        message = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/strong").text
        print message
        #Check validations message
        self.assertEqual(message, "Authentication Failed")




    @classmethod
    def tearDownClass(cls):

        #cls.driver.close()
        #cls.driver.quit()

        print("success")


if __name__ == '__main__':
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='C:/Users/ss112148/PycharmProjects/dt-fanx/reports'))
    #unittest.main()