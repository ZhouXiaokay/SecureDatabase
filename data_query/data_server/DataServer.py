from typing import Set, Dict, Tuple, List

import transmission.tenseal.tenseal_data_server_pb2_grpc as tenseal_data_server_pb2_grpc
import transmission.tenseal.tenseal_data_server_pb2 as tenseal_data_server_pb2
import transmission.tenseal.tenseal_key_server_pb2_grpc as tenseal_key_server_pb2_grpc
import tenseal as ts
from data_query.data_server.conn_mysql import *
import pickle
import grpc

class DatabaseServer(tenseal_data_server_pb2_grpc.DatabaseServerServiceServicer):

    def __init__(self, key_server_address, pk_ctx_file, sk_ctx_file, db_name, cfg):
        self.ks_address = key_server_address
        pk_bytes = open(pk_ctx_file, "rb").read()
        self.pk_ctx = ts.context_from(pk_bytes)
        ctx_byte = open(sk_ctx_file, "rb").read()
        self.sk_ctx = ts.context_from(ctx_byte)
        self.max_msg_size = 1000000000
        self.options = [('grpc.max_send_message_length', self.max_msg_size),
                        ('grpc.max_receive_message_length', self.max_msg_size)]

        self.sleep_time = 0.01
        self.name = db_name
        self.cfg = cfg
        self.n_th_cache: Dict[int,Tuple[int,float]] = {}
        self.hash_cache: Dict[int,Tuple[int,float]] = {}


    def query_operation(self, request, context):
        sql = generate_sql(request)
        query_result = get_query_results(self.name, self.cfg, sql)

        plain_vector = ts.plain_tensor(query_result)
        enc_vector = ts.ckks_vector(self.pk_ctx, plain_vector)
        serialize_msg = enc_vector.serialize()

        response = tenseal_data_server_pb2.enc_query_result(enc_result=serialize_msg)

        return response

    def noise_query_operation(self, request, context):
        sql = generate_sql(request)
        cid = request.cid
        qid = request.qid
        channel = grpc.insecure_channel(self.ks_address, options=self.options)
        key_stub = tenseal_key_server_pb2_grpc.KeyServerServiceStub(channel)

        query_result = get_noise_query_results(self.name, self.cfg, cid, qid, sql, key_stub)
        serialize_msg = pickle.dumps(query_result)

        response = tenseal_data_server_pb2.enc_query_result(enc_result=serialize_msg)

        return response

    def n_th_query_operation(self, request, context):
        cid = request.cid
        qid = request.qid
        n = request.n
        mode = request.mode
        table_name = request.table_name
        column_name = request.column_name
        if mode == "clean":
            self.n_th_cache.clear()
            self.hash_cache.clear()
            print("cid: ", cid, " qid: ", qid, " n: ", n, " mode: ", mode)
            sql = "SELECT {1},COUNT(*) AS i FROM {0} GROUP BY {1} ORDER BY i".format("database_" + self.name + "." +table_name, column_name)
            print(sql)
            query_result = get_query_results(self.name, self.cfg, sql)
            print(query_result)
            for i in range(len(query_result)):
                self.n_th_cache[i] = query_result[i]
                self.hash_cache[hash(query_result[i][0] + 0.01)] = query_result[i]

        available = False

        if n in self.n_th_cache:
            available = True
            query_result = [self.n_th_cache[n][1]]
            hash_value = hash(self.n_th_cache[n][0] + 0.01)
        else:
            hash_value = 0
            query_result = [0]

        if n > len(self.n_th_cache):
            available = False

        plain_vector = ts.plain_tensor(query_result)
        enc_vector = ts.ckks_vector(self.pk_ctx, plain_vector)
        serialize_msg = enc_vector.serialize()
        response = tenseal_data_server_pb2.n_th_query_result(cid=request.cid, qid=request.qid,n = n,hash = hash_value ,result = serialize_msg,available = available)
        return response

    def query_from_buffer(self, request, context):
        hash_ = request.hash
        available = False
        if hash_ in self.hash_cache:
            available = True
            query_result = [self.hash_cache[hash_][1]]
        else:
            query_result = [0]

        plain_vector = ts.plain_tensor(query_result)
        enc_vector = ts.ckks_vector(self.pk_ctx, plain_vector)
        serialize_msg = enc_vector.serialize()

        response = tenseal_data_server_pb2.query_result_result(result = serialize_msg,available = available)

        return response

    def query_mode_using_hash(self, request, context):
        hash_ = request.hash
        import pickle
        hash_ = pickle.loads(hash_)

        # init available_list with False
        available_list = [False] * len(hash_)

        query_result = [0] * len(hash_)

        print("query_mode_using_hash: ", hash_)

        for i in range(len(hash_)):
            if hash_[i] in self.hash_cache:
                available_list[i] = True
                query_result[i] = self.hash_cache[hash_[i]][0]

        result_list = []

        print("query_mode_using_hash: ", query_result)

        for i in range(len(query_result)):
            plain_vector = ts.plain_tensor([query_result[i]])
            enc_vector = ts.ckks_vector(self.pk_ctx, plain_vector)
            serialize_msg = enc_vector.serialize()
            result_list.append(serialize_msg)

        return tenseal_data_server_pb2.query_mode_using_hash_result(mode = pickle.dumps(result_list),available = pickle.dumps(available_list))

    def query_median_posi(self, request, context):
        cid = request.cid
        qid = request.qid
        table_name = request.table_name
        column_name = request.column_name
        median = request.median
        enc_vector = ts.ckks_vector_from(self.sk_ctx, median)
        dec_vector = enc_vector.decrypt()
        median = dec_vector[0]
        avg = request.avg
        enc_vector = ts.ckks_vector_from(self.sk_ctx, avg)
        dec_vector = enc_vector.decrypt()
        avg = dec_vector[0]
        std = request.std
        enc_vector = ts.ckks_vector_from(self.sk_ctx, std)
        dec_vector = enc_vector.decrypt()
        std = dec_vector[0]
        sigma3_left = avg - 3 * std
        sigma3_right = avg + 3 * std

        le_sql = "SELECT COUNT(*) FROM {0} WHERE {1} <= {2}".format("database_" + self.name + "." +table_name, column_name, median)
        le_result = get_query_results(self.name, self.cfg, le_sql)

        g_sql = "SELECT COUNT(*) FROM {0} WHERE {1} > {2}".format("database_" + self.name + "." +table_name, column_name, median)
        g_result = get_query_results(self.name, self.cfg, g_sql)
        print("le_result: ", le_result, " g_result: ", g_result,median)
        le_result = ts.plain_tensor(le_result)
        g_result = ts.plain_tensor(g_result)
        le_enc_vector = ts.ckks_vector(self.pk_ctx, le_result)
        g_enc_vector = ts.ckks_vector(self.pk_ctx, g_result)

        msg = tenseal_data_server_pb2.query_median_posi_result(less_e = le_enc_vector.serialize(), greater = g_enc_vector.serialize())
        return msg

    def get_count(self, request, context):
        table_name = request.table_name
        column_name = request.column_name
        sql = "SELECT COUNT(*) FROM {0}".format("database_" + self.name + "." +table_name)
        query_result = get_query_results(self.name, self.cfg, sql)
        plain_vector = ts.plain_tensor(query_result)
        enc_vector = ts.ckks_vector(self.pk_ctx, plain_vector)
        serialize_msg = enc_vector.serialize()
        response = tenseal_data_server_pb2.query_result_result(result = serialize_msg)
        return response

    def get_nearest(self, request, context):
        table_name = request.table_name
        column_name = request.column_name
        value = request.value
        enc_vector = ts.ckks_vector_from(self.sk_ctx, value)
        dec_vector = enc_vector.decrypt()
        value = dec_vector[0]
        sql = "SELECT * FROM {0} ORDER BY ABS({1} - {2}) LIMIT 2;".format("database_" + self.name + "." +table_name,value, column_name)
        query_result = get_query_results(self.name, self.cfg, sql)
        if len(query_result) == 0:
            response = tenseal_data_server_pb2.query_nearest_msg(value1 = 0, value2 = 0, count = 0)
        elif len(query_result) == 1:
            plain_vector1 = ts.plain_tensor(query_result[0])
            enc_vector1 = ts.ckks_vector(self.pk_ctx, plain_vector1)
            response = tenseal_data_server_pb2.query_nearest_msg(value1 = enc_vector1.serialize(), value2 = 0, count = 1)
        else:
            plain_vector1 = ts.plain_tensor(query_result[0])
            enc_vector1 = ts.ckks_vector(self.pk_ctx, plain_vector1)
            plain_vector2 = ts.plain_tensor(query_result[1])
            enc_vector2 = ts.ckks_vector(self.pk_ctx, plain_vector2)
            response = tenseal_data_server_pb2.query_nearest_msg(value1 = enc_vector1.serialize(), value2 = enc_vector2.serialize(), count = 2)
        return response
