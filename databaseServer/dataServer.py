import transmission.tenseal.tenseal_data_pb2_grpc as tenseal_data_pb2_grpc
import transmission.tenseal.tenseal_data_pb2 as tenseal_data_pb2
import tenseal as ts
from databaseServer.conn_mysql import *


class DatabaseServer(tenseal_data_pb2_grpc.DatabaseServerServiceServicer):

    def __init__(self, address, pk_ctx_file, name):
        self.address = address
        pk_bytes = open(pk_ctx_file, "rb").read()
        self.pk_ctx = ts.context_from(pk_bytes)
        self.sleep_time = 0.01
        self.name = name

    def QueryOperation(self, request, context):
        sql = generateSQL(request)

        query_result = getQueryResult(self.name, sql)

        plain_vector = ts.plain_tensor(query_result)
        enc_vector = ts.ckks_vector(self.pk_ctx, plain_vector)
        serialize_msg = enc_vector.serialize()

        response = tenseal_data_pb2.responseEncResult(encResult=serialize_msg)

        return response
