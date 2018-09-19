# send email to owners of projects
# Microscope operator if you have been lazy and did not open an account
# you are in trouble
import sqlite3
from glob import glob
from os.path import normpath, basename

PROJECT_HOME = '/home/scipionuser/OffloadData'
TABULIST = ['2018_05_25_rmarabini_smalltestdatasetNOBORRAR',
            '2018_09_18_administrator_22']
DBNAME='/home/scipionuser/webservices/EMadmin/src/db.sqlite3'
# get list of project directories

def _print(list, msg):
    # uncomment for testing
    for item in list:
        print msg, item
    return

def checkProjectDirectory():
    directoryList = glob("%s/2???_??_??_*/" % PROJECT_HOME)
    directoryList = [basename(normpath(item))
                     for item in directoryList if item not in TABULIST]

    _print(directoryList, "checkProjectDirectory")
    return directoryList

# filter through tabu
def applyTabuDirectory(directoryList):
    directoryList = [item for item in directoryList if item not in TABULIST]
    _print(directoryList, "applyTabuDirectory")
    return directoryList

# get emails from database
def getEmails(directoryList):
    """
    select projname, email
    from create_proj_acquisition join authtools_user
    where projname='2018_08_24_carolina_e_dyp' AND
          user_id=authtools_user.id;
    """
    sqlWhereCommand = 'WHERE user_id=authtools_user.id'
    sqlWhereCommand += ' AND ( projname = %s ' % directoryList[0]
    for dir in directoryList[1:]:
        sqlWhereCommand += " OR\n"
        sqlWhereCommand += 'projname = %s)' % dir
    sqlWhereCommand += ')'
    print 'sqlWhereCommand', sqlWhereCommand
    conn = sqlite3.connect(DBNAME)
    c = conn.cursor()
    c.execute('SELECT * FROM {tn} WHERE {cn}="Hi World"'. \
              format(tn=table_name, cn=column_2))
    all_rows = c.fetchall()
    conn.close()


# send email complaining

directoryList = checkProjectDirectory()
applyTabuDirectory(directoryList)