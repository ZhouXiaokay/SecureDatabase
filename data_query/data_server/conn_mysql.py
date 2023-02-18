import pymysql
import numpy as np
import transmission.tenseal.tenseal_key_server_pb2 as tenseal_key_server_pb2
import pickle
import re
from omegaconf import DictConfig

"""
conn_mysql.py provides query operations over database:
1. get max value
2. get min value
3. get sum value
"""


# establish connection with mysql
def conn(name, cfg: DictConfig):
    db = pymysql.connect(host=cfg.database.host,
                         port=int(cfg.database.port),
                         user=cfg.database.user,
                         password=cfg.database.password,
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
    table_name = request.table_name
    column_name = request.column_name
    op = request.op.upper()
    op_sql = parse_op(op, column_name)
    sql = "SELECT " + op_sql + " FROM {0}".format(table_name)

    return sql


# get query result from database_dbname
def get_query_results(db_name, cfg, sql):
    result_list = []
    db = conn(db_name, cfg)
    cursor = db.cursor()
    cursor.execute(sql)
    if "GROUP BY" in sql:
        results = cursor.fetchall()
        for row in results:
            result_list.append((row[0],float(row[1])))
        db.close()
        return result_list

    results = cursor.fetchone()
    # close conn
    db.close()
    for i in range(len(results)):
        result_list.append(float(results[i]))

    return result_list


# get the query results with laplace noise
def get_noise_query_results(db_name, cfg, cid, qid, sql, key_stub):
    # sensitivity = 1
    # epsilon = 5
    # noise = np.random.laplace(loc=0, scale=sensitivity / epsilon)
    noise_request = tenseal_key_server_pb2.get_noise_request(db_name=db_name, cid=cid, qid=qid)
    response = key_stub.get_noise(noise_request)
    noise_msg = response.noise_msg
    noise = pickle.loads(noise_msg)

    result_list = get_query_results(db_name, sql)
    noise_result = np.add(result_list, noise).tolist()

    return noise_result
