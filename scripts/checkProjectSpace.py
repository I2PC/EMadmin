# send email to owners of projects
# Microscope operator if you have been lazy and did not open an account
# you are in trouble
from glob import glob
PROJECT_HOME = '/home/scipionuser/OffloadData'
TABULIST = ['2018_06_25_foo_wwqeqweqw/', '2018_06_18_foo_ribosome/']
DBNAME=''
# get list of project directories
def checkProjectDirectory():
    directoryList = glob("%s/2???_??_??_*/" % PROJECT_HOME)
    return directoryList

# filter through tabu
def applyTabuDirectory(directoryList):
    return [item for item in directoryList if item not in TABULIST]

# get emails from database
def getEmails(directoryList):

# send email complaining

checkProjectDirectory()