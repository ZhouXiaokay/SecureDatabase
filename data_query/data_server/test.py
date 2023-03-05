import re
import tenseal as ts
import numpy as np

def parse_op(op, column_name):
    column_name = '(' + column_name + ')'
    op_sql = ''
    pattern = r'[+,\-,*,/,(,)]'
    func_list = [i for i in re.split(pattern, op) if i != '']
    op_list = re.findall(pattern, op)
    print(func_list)
    print(op_list)
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
                    print(j)
                else:
                    j += 1
            else:
                j += 1
            print(op_sql)
    else:
        for i in range(len(func_list)):
            if func_list[i].isdigit():
                op_sql = op_sql + func_list[i] + op_list[i]
            else:
                if i < len(op_list):
                    op_sql = op_sql + func_list[i] + column_name + op_list[i]
                else:
                    op_sql = op_sql + func_list[i] + column_name
    op_sql=op_sql.upper()
    return op_sql


ctx_bytes = open('../../transmission/ts_ckks.config', 'rb').read()
ctx = ts.context_from(ctx_bytes)
vec_1 = [10893537.6585275]
vec_2 = [1.0344827589305388]
result_list = []
plain_vec_1 = ts.plain_tensor(vec_1)
plain_vec_2 = ts.plain_tensor(vec_2)
enc_1 = ts.ckks_vector(ctx,plain_vec_1)
enc_2 = ts.ckks_vector(ctx,plain_vec_2)

mul_enc =enc_1*enc_2
print(mul_enc.decrypt())
