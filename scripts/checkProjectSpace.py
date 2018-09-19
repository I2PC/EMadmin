# send email to owners of projects
# Microscope operator if you have been lazy and did not open an account
# you are in trouble
from glob import glob
PROJECT_HOME = '/home/scipionuser/OffloadData'
TABULIST = ['/home/scipionuser/OffloadData/2018_05_25_rmarabini_smalltestdatasetNOBORRAR/',
            '/home/scipionuser/OffloadData/2018_09_18_administrator_22']
DBNAME=''
# get list of project directories
def _print(list, msg):
    for item in list:
        print msg, item

def checkProjectDirectory():
    directoryList = glob("%s/2???_??_??_*/" % PROJECT_HOME)
    _print(directoryList, "checkProjectDirectory")
    return directoryList

# filter through tabu
def applyTabuDirectory(directoryList):
    directoryList = [item for item in directoryList if item not in TABULIST]
    _print(directoryList, "applyTabuDirectory")
    return directoryList

# get emails from database
def getEmails(directoryList):
    pass

# send email complaining

directoryList = checkProjectDirectory()
applyTabuDirectory(directoryList)