import pymysql

def conn():
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='199966',
                         database='database_1')
    return db



def getMaxValue(name):
    db = conn()
    cursor = db.cursor()
    sql = "SELECT MAX(value) FROM DATA_{0}".format(name)
    cursor.execute(sql)
    results = cursor.fetchone()

    # close conn
    db.close()
    return results[0]

