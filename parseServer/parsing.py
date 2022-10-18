"""
parsing.py responses to parse the request from clients,
and return results
"""
from parseServer.utils import *


def requestParsing(data_stub, request, pk_ctx):
    db_name = request.db_name.upper()
    # stub = stubDict[db_name]
    query_request = tenseal_data_pb2.requestOP(op=request.op, column_name=request.column_name,
                                               table_name=request.table_name)
    response = data_stub.QueryOperation(query_request)
    enc_vector = ts.ckks_vector_from(pk_ctx, response.encResult)

    return enc_vector
