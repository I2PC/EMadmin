# send email to owners of projects
# Microscope operator if you have been lazy and did not open an account
# you are in trouble
from glob import glob
PROJECT_HOME = '/home/scipionuser/OffloadData'
TABULIST = ['2018_06_25_foo_wwqeqweqw/', '2018_06_18_foo_ribosome/']
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
    _print(applyTabuDirectory, "checkProjectDirectory")
    return directoryList

# get emails from database
def getEmails(directoryList):
    pass

# send email complaining

checkProjectDirectory()