import transmission.tenseal.tenseal_data_server_pb2_grpc as tenseal_data_server_pb2_grpc
import transmission.tenseal.tenseal_data_server_pb2 as tenseal_data_server_pb2
import transmission.tenseal.tenseal_key_server_pb2_grpc as tenseal_key_server_pb2_grpc
import tenseal as ts
from data_query.data_server.conn_mysql import *
import pickle
import grpc


class DatabaseServer(tenseal_data_server_pb2_grpc.DatabaseServerServiceServicer):

    def __init__(self, key_server_address, pk_ctx_file, db_name, cfg):
        self.ks_address = key_server_address
        pk_bytes = open(pk_ctx_file, "rb").read()
        self.pk_ctx = ts.context_from(pk_bytes)
        self.max_msg_size = 1000000000
        self.options = [('grpc.max_send_message_length', self.max_msg_size),
                        ('grpc.max_receive_message_length', self.max_msg_size)]

        self.sleep_time = 0.01
        self.name = db_name
        self.cfg = cfg

    def query_operation(self, request, context):
        sql = generate_sql(request)
        query_result = get_query_results(self.name, self.cfg, sql)

        plain_vector = ts.plain_tensor(query_result)
        enc_vector = ts.ckks_vector(self.pk_ctx, plain_vector)
        serialize_msg = enc_vector.serialize()

        response = tenseal_data_server_pb2.query_result(enc_result=serialize_msg)

        return response

    def noise_query_operation(self, request, context):
        sql = generate_sql(request)
        cid = request.cid
        qid = request.qid
        channel = grpc.insecure_channel(self.ks_address, options=self.options)
        key_stub = tenseal_key_server_pb2_grpc.KeyServerServiceStub(channel)

        query_result = get_noise_query_results(self.name, self.cfg, cid, qid, sql, key_stub)
        serialize_msg = pickle.dumps(query_result)

        response = tenseal_data_server_pb2.query_result(enc_result=serialize_msg)

        return response
