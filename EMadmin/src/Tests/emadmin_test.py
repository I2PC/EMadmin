# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, os
from collections import OrderedDict
from loremipsum import get_paragraphs, get_sentences
import sqlite3

class onLineShopTester(unittest.TestCase):
    username    = "testUser1"
    passwd      = "passwd1"
    institution = "intitution1"
    email       = "%s@gmail.com"%username
    sample      = "sample1"
    base_url    = "http://127.0.0.1:8000/"
    admin_url   = base_url + "admin/"
    database    = "db.sqlite3"

    chromeDriver = "/usr/local/bin/chromedriver"

    def setUp(self):
#        self.driver = webdriver.Firefox()
        self.driver = webdriver.Chrome(self.chromeDriver)

    def find_element_by_id(self,_id,value,waitFor=1):
        self.driver.find_element_by_id(_id).clear()
        self.driver.find_element_by_id(_id).send_keys(value)
        time.sleep(waitFor)

    def find_element_by_xpath(self,_xpath,waitFor=1):
        self.driver.find_element_by_xpath(_xpath).click()
        time.sleep(waitFor)

    def find_element_by_name(self,_name,waitFor=1):
        self.driver.find_element_by_name(_name).click()
        time.sleep(waitFor)

    def find_element_by_link_text(self,_name,waitFor=1):
        self.driver.find_element_by_link_text(_name).click()
        time.sleep(waitFor)

    def pullDownMenuById(self,id, value, waitFor=1):
        select = Select(self.driver.find_element_by_id(id))
        select.select_by_value(value)
        time.sleep(waitFor)

    def signUp(self):
        self.find_element_by_xpath("//a[@class='btn btn-primary'][1]")
        self.find_element_by_id("id_email",self.email)
        self.find_element_by_id("id_name",self.username)
        self.find_element_by_id("id_password1",self.passwd)
        self.find_element_by_id("id_password2",self.passwd)
        self.find_element_by_id("id_institution",self.institution)
        self.find_element_by_xpath("//input[@type='submit' and @value='Sign up']")

    def signOut(self):
        # open pull down menu
        self.find_element_by_xpath("//ul[@class='nav navbar-nav navbar-right'][1]")
        # select logout
        self.find_element_by_xpath("//ul[@class='dropdown-menu'][1]")

    def signIn(self):
        #self.driver.find_element_by_link_text("Log in").click()
        self.find_element_by_xpath("//a[@class='btn btn-default'][1]")
        self.find_element_by_id("id_username",self.email)
        self.find_element_by_id("id_password",self.passwd)
        self.find_element_by_xpath("//input[@type='submit' and @value='Log in']")

    def createProject1(self):
        # Microscope
        self.find_element_by_link_text("Create_Project")
        self.find_element_by_id("id_sample",self.sample)
        self.find_element_by_id("id_voltage",200)
        self.find_element_by_id("id_shiftLength",2)
        self.find_element_by_id("id_backupPath","/media/roberto/b3ab7bfb-85ee-4dd7-8cd3-a61070d03d96")
        self.find_element_by_xpath("//input[@type='submit' and @value='Create Project']")

    def createProject2(self):
        #acquisition params
        self.find_element_by_id("id_nominal_magnification", "70000,0")
        self.find_element_by_id("id_sampling_rate", "1.34")
        self.find_element_by_id("id_spotsize", 2)
        self.find_element_by_id("id_illuminated_area", "1.68")
        # Dose & Fractions
        self.find_element_by_id("id_dose_per_fraction", 2)
        self.find_element_by_id("id_total_exposure_time", 15)
        self.find_element_by_id("id_number_of_fractions", 15)
        self.find_element_by_id("id_frames_in_fraction", 3)
        # EPU parameters
        self.find_element_by_id("id_nominal_defocus_range", "1 2 3")
        self.find_element_by_id("id_autofocus_distance", 5)
        self.pullDownMenuById('id_drift_meassurement','always')
        self.find_element_by_id("id_delay_after_stage_shift", 5)
        self.find_element_by_id("id_max_image_shift", 5)
        self.pullDownMenuById('id_exposure_hole','2')
        self.pullDownMenuById('id_c2','50')
        self.pullDownMenuById('id_o1','70')
        self.pullDownMenuById('id_php','3')
        #PRESS BOTTON
        self.find_element_by_xpath("//input[@type='submit' and @value='Launch Scipion']")

    def seeHome(self, waitFor=1):
        #print "self.base_url", self.base_url
        self.driver.get(self.base_url)
        time.sleep(waitFor)

    def quit(self, waitFor=1):
        time.sleep(waitFor)
        self.driver.quit()

    def deleteUser(self, email):
        try:
            conn = sqlite3.connect(self.database)
            cur = conn.cursor()
            sql = """DELETE FROM authtools_user
                     WHERE email='%s'"""%email
            cur.execute(sql)
            conn.commit()
        except Exception as e:
            print (e)

    def deleteProjectFromUser(self, email):
        try:
            conn = sqlite3.connect(self.database)
            cur = conn.cursor()
            sql = """SELECT id FROM authtools_user
                     WHERE email='%s'"""%email
            cur.execute(sql)
            user_id = cur.fetchone()[0]
            sql = """DELETE FROM create_proj_acquisition
                     WHERE user_id='%d'"""%user_id
            cur.execute(sql)
            conn.commit()
        except Exception as e:
            print (e)

    def test_emadmin(self):
        ##self.deleteUser(self.email)
        self.seeHome(2)
        ##self.signUp()  # create user
        ##self.signOut()  # log out
        self.deleteProjectFromUser(self.email)
        self.signIn()  # log in
        self.createProject1()  # first form
        self.createProject2()  # first form


        #close browser
        self.quit(2)

if __name__ == "__main__":
    unittest.main()

