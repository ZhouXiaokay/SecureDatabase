import pymysql

"""
conn_mysql.py provides 
"""

# establish connection with mysql
def conn():
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='199966',
                         database='database_1')
    return db


# get max value from table_name
def getMaxValue(name):
    db = conn()
    cursor = db.cursor()
    sql = "SELECT MAX(value) FROM DATA_{0}".format(name)
    cursor.execute(sql)
    results = cursor.fetchone()
    # close conn
    db.close()
    return results[0]


# get sum value from table_name
def getSumValue(name):
    db = conn()
    cursor = db.cursor()
    sql = "SELECT SUM(value) FROM DATA_{0}".format(name)
    cursor.execute(sql)
    results = cursor.fetchone()
    # close conn
    db.close()
    return results[0]


def getMinValue(name):
    db = conn()
    cursor = db.cursor()
    sql = "SELECT MIN(value) FROM DATA_{0}".format(name)
    cursor.execute(sql)
    results = cursor.fetchone()
    # close conn
    db.close()
    return results[0]

def getSumValue(name):
    db = conn()
    cursor = db.cursor()
    sql = "SELECT SUM(value) FROM DATA_{0}".format(name)
    cursor.execute(sql)
    results = cursor.fetchone()
    # close conn
    db.close()
    return results[0]
