"""
parsing.py responses to parse the request from clients,
and return results
"""
from parseServer.utils import *


# parse the request from clientProxy, divided into two schemes:local and total
def requestParsing(request, pk_ctx, address_dict, options):
    db_name = request.db_name.upper()

    if db_name == "TOTAL":
        op = request.op.upper()
        stub_list = getAllDBStub(address_dict, options)

        enc_vector = processTotalRequest(op, request, stub_list, pk_ctx)
        return enc_vector

    else:
        data_stub = getDBStub(request.db_name, address_dict, options)
        query_request = tenseal_data_pb2.requestOP(op=request.op, column_name=request.column_name,
                                                   table_name=request.table_name)
        response = data_stub.QueryOperation(query_request)
        enc_vector = ts.ckks_vector_from(pk_ctx, response.encResult)

        return enc_vector


# process the request which needs all dataServer participates
def processTotalRequest(op, request, stub_list, pk_ctx):
    if op == "SUM":
        sum_enc_vector = getSumTotal(request, stub_list, pk_ctx)
        return sum_enc_vector

    if op == "COUNT":
        count_enc_vector = getCountTotal(request, stub_list, pk_ctx)
        return count_enc_vector
    # unfinished
    if op == "AVG":
        sum_enc_vector = getSumTotal(request, stub_list, pk_ctx)
        count_enc_vector = getCountTotal(request, stub_list, pk_ctx)
        avg_enc_vector = sum_enc_vector / count_enc_vector
        return avg_enc_vector


# get sum from all databaseServer
def getSumTotal(request, stub_list, pk_ctx):
    query_request = tenseal_data_pb2.requestOP(op="sum", column_name=request.column_name,
                                               table_name=request.table_name)
    sum_list = []
    for stub in stub_list:
        response = stub.QueryOperation(query_request)
        enc_vector = ts.ckks_vector_from(pk_ctx, response.encResult)
        sum_list.append(enc_vector)
    sum_enc_vector = sum(sum_list)
    return sum_enc_vector


# get count from all databaseServer
def getCountTotal(request, stub_list, pk_ctx):
    query_request = tenseal_data_pb2.requestOP(op="count", column_name=request.column_name,
                                               table_name=request.table_name)
    count_list = []
    for stub in stub_list:
        response = stub.QueryOperation(query_request)
        enc_vector = ts.ckks_vector_from(pk_ctx, response.encResult)
        count_list.append(enc_vector)
    count_enc_vector = sum(count_list)
    return count_enc_vector
