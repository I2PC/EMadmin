# send email to owners of projects
# Microscope operator if you have been lazy and did not open an account
# you are in trouble
import sqlite3, time, os, stat, datetime

from glob import glob
from os.path import normpath, basename

PROJECT_HOME = '/home/scipionuser/OffloadData'
TABULIST = ['2018_05_25_rmarabini_smalltestdatasetNOBORRAR',
            '2018_09_18_administrator_22']
DBNAME='/home/scipionuser/webservices/EMadmin/src/kk.sqlite3'
TWOWEEKS=1209600

# get list of project directories

class Project():
    def __init__(self, abspath):
        self.abspath = abspath
        self.projectName = basename(normpath(abspath))
        self.lastModificationSeconds = os.stat(abspath)[stat.ST_MTIME]  # secs
        self.email = None

    def __str__(self):
        if self.email is not None:
            return "%s (%s) %d" % (self.projectName,
                                   self.email,
                                   self.lastModificationSeconds)
        else:
            return "%s %d" % (self.projectName,
                              self.lastModificationSeconds)

    def isOldProject(self):
        return (time.time() - self.lastModificationSeconds) > TWOWEEKS

    def isNotInTabuList(self):
        return self.projectName  not in TABULIST

def _print(list, msg):
    # uncomment for testing
    print msg
    for item in list:
        print item
    return

def getProjecs():
    # get project list
    directoryList = glob("%s/2???_??_??_*/" % PROJECT_HOME)
    projectList = [Project(item) for item in directoryList]
    directoryList = None  # free memory
    _print(projectList, "initial list")
    # remove new projects
    projectList = [item for item in projectList if item.isOldProject()]
    # remove directories in tabu list
    projectList = [item for item in projectList if item.isNotInTabuList()]
    _print(projectList, "final list")
    return projectList

# get emails from database
def getEmails(directoryList):
    """
    select projname, email
    from create_proj_acquisition join authtools_user
    where projname='2018_08_24_carolina_e_dyp' AND
          user_id=authtools_user.id;
    """
    sqlWhereCommand  = '''SELECT projname, email, date(date) as date
FROM create_proj_acquisition join authtools_user\n'''
    sqlWhereCommand += 'WHERE user_id=authtools_user.id AND\n'
    sqlWhereCommand += "    ((projname = '%s')" % directoryList[0].projectName
    for dir in directoryList[1:]:
        sqlWhereCommand += " OR\n"
        sqlWhereCommand += "     (projname = '%s')" % dir.projectName
    sqlWhereCommand += ')'
    try:
        conn = sqlite3.connect(DBNAME)
    except:
        print "Can not connect to database %s"%DBNAME

    c = conn.cursor()
    c.execute(sqlWhereCommand)
    rows = c.fetchall()
    conn.close()
    return  rows

def sendEmails(rows):
    today = datetime.date.today()
    week = datetime.timedelta(days=7)
    msg = """Dear user,

    I am writting you regarding the project named %s
    created on %s. The data files related with this project
    and stored in the CryoEM facility will be deleted on %s.

    Yours faithfully.

        CNB CryoEM Facility Staff"""

    for row in rows:
        print msg % (row[0], row[2], str(today + week))


# send email complaining

projectList = getProjecs()
rows = getEmails(projectList)
sendEmails(rows)