# -*- coding: utf-8 -*-
# source ~/webservices/EMadmin/virEMadmin/bin/activate
# cd /home/scipionuser/webservices/EMadmin/src
# python manage.py runserver
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
import shutil
from glob import glob

class onLineShopTester(unittest.TestCase):
    num         = 1
    username    = "testUser%d"% num
    passwd      = "passwd%d"% num
    institution = "CNB-CSIC\\C/ Darwin 3\\28049 Madrid\\Espa\~{n}a"
    email       = "%s@gmail.com"%username
    sample      = "sample%d"% num
    base_url    = "http://127.0.0.1:8000/"
    admin_url   = base_url + "admin/"
    database    = "db.sqlite3"

    num          = 100
    usernameA    = "testUser%d"% num
    passwdA      = "passwd%d"% num
    institutionA = "CNB-CSIC\\C/ Darwin 3\\28049 Madrid\\Espa\~{n}a"
    emailA       = "%s@gmail.com"%usernameA


    chromeDriver = "/usr/local/bin/chromedriver"
    #chromeDriver = "/home/roberto/bin/chromedriver"

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

    def signIn(self, email, passwd):
        #self.driver.find_element_by_link_text("Log in").click()
        self.find_element_by_xpath("//a[@class='btn btn-default'][1]")
        self.find_element_by_id("id_username", email)
        self.find_element_by_id("id_password", passwd)
        self.find_element_by_xpath("//input[@type='submit' and @value='Log in']")

    def createProject1(self):
        # Microscope
        self.find_element_by_link_text("Project")
        self.pullDownMenuById('id_workflow','2')
        self.pullDownMenuById('id_workflow','3')
        self.pullDownMenuById('id_workflow','1')
        self.find_element_by_id("id_sample",self.sample)
        self.find_element_by_id("id_voltage",200)
        self.find_element_by_id("id_shiftLength",2)
        self.find_element_by_id("id_backupPath","/media/roberto")
        self.find_element_by_xpath("//input[@type='submit' and @value='Create Project']")

    def createProject2(self):
        #acquisition params
        self.find_element_by_id("id_nominal_magnification", "70000,0")
        self.find_element_by_id("id_sampling_rate", "1.42")
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
        self.find_element_by_id("id_delay_after_image_shift", 5)
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
            sql = """SELECT projname FROM create_proj_acquisition
                     WHERE user_id=%d"""%user_id
            cur.execute(sql)
            projname = cur.fetchone()[0]
            sql = """DELETE FROM create_proj_acquisition
                     WHERE user_id='%d'"""%user_id
            cur.execute(sql)
            conn.commit()
            shutil.rmtree(os.path.join(os.environ['HOME'], "ScipionUserData",
                                       "projects", projname))
        except Exception as e:
            print (e)

    def deleteConcept(self):
        try:
            conn = sqlite3.connect(self.database)
            cur = conn.cursor()
            sql = """DELETE FROM invoice_concept"""
            cur.execute(sql)
            conn.commit()
        except Exception as e:
            print (e)

    def deleteInvoice(self):
        try:
            conn = sqlite3.connect(self.database)
            cur = conn.cursor()
            sql = """DELETE FROM invoice_invoice"""
            cur.execute(sql)
            conn.commit()
        except Exception as e:
            print (e)

    def deleteInvoiceLines(self):
        try:
            conn = sqlite3.connect(self.database)
            cur = conn.cursor()
            sql = """DELETE FROM invoice_invoiceline"""
            cur.execute(sql)
            conn.commit()
        except Exception as e:
            print (e)


    def simulateAcquisition(self, outputDir='GRID_01/DATA/Images-Disc1/GridSquare_9124395/DATA'):
        """/home/scipionuser/OffloadData/2017_10_19_fcojavierchichon_qwerty/GRID_01/DATA/Images-Disc1/GridSquare_9124395/DATA"""
        
        try:
            conn = sqlite3.connect(self.database)
            cur = conn.cursor()
            sql = """SELECT projname, date 
                     FROM create_proj_acquisition
                     WHERE date IN   (SELECT MAX(date) 
                                      FROM create_proj_acquisition);"""
            cur.execute(sql)
            projName = cur.fetchone()[0]
        except Exception as e:
            print (e)
        time.sleep(20)  # wait here until Scipion is started
        fullProjectPath =  os.path.join("/home/scipionuser/OffloadData", projName,outputDir)
        print fullProjectPath
        if os.path.exists(fullProjectPath):
            shutil.rmtree(fullProjectPath) # clean path
        os.makedirs(fullProjectPath)  # create output dir
        INPUTDAT="/home/OffloadData/2018_01_18_fabrizio_d1_1801_/GRID_??/DATA/Images-Disc1/GridSquare_*/Data/FoilHole_*_Fractions.mrc"
        inputFiles = glob(INPUTDAT)

        aTime = 90  # 90 sec per movie
        counter = 0
        for f in inputFiles:
            outputPath = os.path.join(fullProjectPath, os.path.basename(f))
            print "%d) Linking %s -> %s" % (counter, f, outputPath)
            counter += 1
            os.symlink(f, outputPath)
            time.sleep(aTime)
    
    def createAdminUser(self, username, email, passwd):
        command = """python ./manage.py createsuperuser2 --name %s --email %s --password %s"""%(username, email, passwd)
        os.system(command)

    def createConcept(self, numConcepts):
        try:
            conn = sqlite3.connect(self.database)
            cur = conn.cursor()
            sql = ''' INSERT INTO invoice_concept(name,unit_price)
              VALUES(?,?) '''
            for i in range (1, numConcepts):
                cur.execute(sql, ('name_%02d'%i, float(i*1.0)))
            conn.commit()
        except Exception as e:
            print (e)


    def test_emadmin(self):
        #clean tables
        self.seeHome(2)
        self.deleteInvoiceLines
        self.deleteInvoice()
        self.deleteConcept()
        self.deleteUser(self.emailA)

        # create administrative user
        self.createAdminUser(self.usernameA, self.emailA, self.passwdA)
        
        # create concepts
        self.createConcept(10)

        # create regular user
        self.deleteProjectFromUser(self.email)
        self.deleteUser(self.email)


        
        self.seeHome(2)
        self.signUp()  # create user
        self.signOut()  # log out
        self.signIn(self.email, self.passwd)  # log in
        #time.sleep(60)
        self.createProject1()  # first form
        self.createProject2()  # first form

        #create invoice
        self.signOut()  # log out
        self.signIn(self.emailA, self.passwdA)
        
#        self.simulateAcquisition()  # link movies
        # create administrative user

        #close browser
        self.quit(2)

if __name__ == "__main__":
    unittest.main()

