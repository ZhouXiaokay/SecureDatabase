import pymysql

"""
conn_mysql.py provides query operations over database:
1. get max value
2. get min value
3. get sum value
"""


# establish connection with mysql
def conn(name):
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='199966',
                         database='database_{0}'.format(name))
    return db


# generate sql from request
def generateSQL(request):
    table_name = request.table_name.upper()
    column_name = request.column_name.upper()
    op = request.op.upper()
    sql = "SELECT {0}({1}) FROM {2}".format(op, column_name, table_name)
    # if op == "AVG-TOTAL":
    #     sql = "SELECT SUM({0}),COUNT({0}) FROM {1}".format(column_name, table_name)

    return sql


# get query result from database_dbname
def getQueryResult(db_name, sql):
    resultl=[]
    db = conn(db_name)
    cursor = db.cursor()
    cursor.execute(sql)
    results = cursor.fetchone()
    # close conn
    db.close()
    for i in range(len(results)):
        resultl.append(results[i])

    return resultl
