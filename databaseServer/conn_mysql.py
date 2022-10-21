import pymysql
import numpy as np
import transmission.request.request_keyServer_pb2 as request_keyServer_pb2
import pickle

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
                         password='99996666',
                         database='database_{0}'.format(name))
    return db


# generate sql from request
def generate_sql(request):
    table_name = request.table_name.upper()
    column_name = request.column_name.upper()
    op = request.op.upper()
    sql = "SELECT {0}({1}) FROM {2}".format(op, column_name, table_name)
    # if op == "AVG-TOTAL":
    #     sql = "SELECT SUM({0}),COUNT({0}) FROM {1}".format(column_name, table_name)

    return sql


# get query result from database_dbname
def get_query_results(db_name, sql):
    resultl = []
    db = conn(db_name)
    cursor = db.cursor()
    cursor.execute(sql)
    results = cursor.fetchone()
    # close conn
    db.close()
    for i in range(len(results)):
        resultl.append(results[i])

    return resultl


# get the query results with laplace noise
def get_noise_query_results(db_name, cid, qid, sql, key_stub):
    # sensitivity = 1
    # epsilon = 5
    # noise = np.random.laplace(loc=0, scale=sensitivity / epsilon)
    noise_request = request_keyServer_pb2.requestGetNoise(db_name=db_name, cid=cid, qid=qid)
    response = key_stub.GetNoise(noise_request)
    noise_msg = response.noiseMsg
    noise = pickle.loads(noise_msg)

    result_list = get_query_results(db_name, sql)
    noise_result = np.add(result_list, noise).tolist()

    return noise_result
