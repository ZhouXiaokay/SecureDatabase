import pymysql
import numpy as np
import transmission.request.request_keyServer_pb2 as request_keyServer_pb2
import pickle
import re

"""
conn_mysql.py provides query operations over database:
1. get max value
2. get min value
3. get sum value
"""


# establish connection with mysql
def conn(name):
    db = pymysql.connect(host='localhost',
                         port=3306,
                         user='root',
                         password='99996666',
                         database='database_{0}'.format(name))
    return db


def parse_op(op, column_name):
    column_name = '(' + column_name + ')'
    op_sql = ''
    pattern = r'[+,\-,*,/,(,)]'
    func_list = [i for i in re.split(pattern, op) if i != '']
    op_list = re.findall(pattern, op)
    if '(' or ')' in op_list:
        j = 0
        for i in range(len(func_list)):
            if func_list[i].isdigit():
                if j < len(op_list):
                    op_sql = op_sql + func_list[i] + op_list[j]
                else:
                    op_sql = op_sql + func_list[i]
            else:
                if j < len(op_list):
                    op_sql = op_sql + func_list[i] + column_name + op_list[j]
                else:
                    op_sql = op_sql + func_list[i] + column_name

            if j + 1 < len(op_list):
                if op_list[j] == ')':
                    op_sql = op_sql + op_list[j + 1]
                    j += 2
                    if op_list[j] == '(':
                        op_sql = op_sql + op_list[j]
                        j += 1
                elif op_list[j + 1] == '(':
                    op_sql = op_sql + op_list[j + 1]
                    j += 2
                else:
                    j += 1
            else:
                j += 1
    else:
        for i in range(len(func_list)):
            if func_list[i].isdigit():
                op_sql = op_sql + func_list[i] + op_list[i]
            else:
                if i < len(op_list):
                    op_sql = op_sql + func_list[i] + column_name + op_list[i]
                else:
                    op_sql = op_sql + func_list[i] + column_name
    op_sql = op_sql.upper()
    return op_sql


# generate sql from request
def generate_sql(request):
    table_name = request.table_name.upper()
    column_name = request.column_name.upper()
    op = request.op.upper()
    op_sql = parse_op(op, column_name)
    sql = "SELECT " + op_sql + " FROM {0}".format(table_name)

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
        resultl.append(float(results[i]))

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
