# send email to owners of projects
# Microscope operator if you have been lazy and did not open an account
# you are in trouble
import sqlite3, time, os,stat

from glob import glob
from os.path import normpath, basename

PROJECT_HOME = '/home/scipionuser/OffloadData'
TABULIST = ['2018_05_25_rmarabini_smalltestdatasetNOBORRAR',
            '2018_09_18_administrator_22']
DBNAME='/home/scipionuser/webservices/EMadmin/src/kk.sqlite3'
TWOWEEKS=1209600

# get list of project directories

def _print(list, msg):
    # uncomment for testing
    for item in list:
        print msg, item
    return


def file_age_in_seconds(pathname):  # since last modificacion
    return (time.time() - os.stat(pathname)[stat.ST_MTIME] > TWOWEEKS)

def getProjectDirectory():
    directoryList = glob("%s/2???_??_??_*/" % PROJECT_HOME)
    _print(directoryList, "input")
    #remove new directories
    directoryList = [item for item in directoryList if file_age_in_seconds(item)]
    _print(directoryList, "remove new dir")
    #remove directory path
    directoryList = [basename(normpath(item)) for item in directoryList]
    _print(directoryList, "remove path")
    # remove directories in tabu list
    directoryList = [item for item in directoryList if item not in TABULIST]
    _print(directoryList, "remove tabu")

    _print(directoryList, "checkProjectDirectory")
    return directoryList

# get emails from database
def getEmails(directoryList):
    """
    select projname, email
    from create_proj_acquisition join authtools_user
    where projname='2018_08_24_carolina_e_dyp' AND
          user_id=authtools_user.id;
    """
    sqlWhereCommand  = '''SELECT projname, email
FROM create_proj_acquisition join authtools_user\n'''
    sqlWhereCommand += 'WHERE user_id=authtools_user.id AND\n'
    sqlWhereCommand += "    ((projname = '%s')" % directoryList[0]
    for dir in directoryList[1:]:
        sqlWhereCommand += " OR\n"
        sqlWhereCommand += "     (projname = '%s')" % dir
    sqlWhereCommand += ')'

    try:
        conn = sqlite3.connect(DBNAME)
    except:
        print "Can not connect to database %s"%DBNAME

    c = conn.cursor()
    c.execute(sqlWhereCommand)
    rows = c.fetchall()
    conn.close()
    return rows

def sendEmails(rows):
    pass #for row in rows:


# send email complaining

directoryList = getProjectDirectory()
rows = getEmails(directoryList)
sendEmails(rows)