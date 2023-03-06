import transmission.tenseal.tenseal_data_server_pb2_grpc as tenseal_data_server_pb2_grpc
import transmission.tenseal.tenseal_data_server_pb2 as tenseal_data_server_pb2
import transmission.tenseal.tenseal_key_server_pb2_grpc as tenseal_key_server_pb2_grpc
import tenseal as ts
from data_query.data_server.conn_mysql import *
import pickle
import grpc
import random
import copy


# from transmission.psi import decode_ids_from_client, encode_and_hash_local_id_use_sk


class DatabaseServer(tenseal_data_server_pb2_grpc.DatabaseServerServiceServicer):

    def __init__(self, key_server_address, pk_ctx_file, db_name, cfg):
        self.ks_address = key_server_address
        pk_bytes = open(pk_ctx_file, "rb").read()
        self.pk_ctx = ts.context_from(pk_bytes)
        self.max_msg_size = 1000000000
        self.options = [('grpc.max_send_message_length', self.max_msg_size),
                        ('grpc.max_receive_message_length', self.max_msg_size)]

        self.sleep_time = 0.01
        # ID PSi
        self.shuffle_seed = random.random()
        # random.seed(self.shuffle_seed)
        self.global_max_id = None
        self.global_min_id = None

        self.name = db_name
        self.cfg = cfg

        # RSA psi
        self.data_server_status = None
        self.rsa_pk = None
        self.rsa_sk = None
        self.rsa_pk_comm_status = False
        self.client_enc_ids_pk = []
        self.client_ra_list = []
        self.client_enc_ids_comm_status = False
        self.client_dec_ids = []
        self.server_hash_enc_ids = []
        self.client_dec_ids_comm_status = False
        self.server_hash_enc_ids_comm_status = False
        self.psi_result = None

    def reset_rsa_psi_status_per_round(self):
        self.rsa_pk = None
        self.rsa_sk = None
        self.rsa_pk_comm_status = False
        self.client_enc_ids_pk = []
        self.client_ra_list = []
        self.client_enc_ids_comm_status = False
        self.client_dec_ids = []
        self.server_hash_enc_ids = []
        self.client_dec_ids_comm_status = False
        self.server_hash_enc_ids_comm_status = False

    def reset_all_rsa_psi_status(self):
        self.data_server_status = None
        self.rsa_pk = None
        self.rsa_sk = None
        self.rsa_pk_comm_status = False
        self.client_enc_ids_pk = []
        self.client_ra_list = []
        self.client_enc_ids_comm_status = False
        self.client_dec_ids = []
        self.server_hash_enc_ids = []
        self.client_dec_ids_comm_status = False
        self.server_hash_enc_ids_comm_status = False
        self.psi_result = None

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

    # ID Psi unencrypted version
    def get_local_max_min_ids(self, id_list):
        return max(id_list), min(id_list)

    def get_shuffled_id_list(self, id_list):
        """
        :param id_list: data id
        :return: origin id list, new index list
        """
        random.seed(self.shuffle_seed)
        mapping_list = []
        origin_list = copy.deepcopy(id_list)
        random.shuffle(id_list)

        for elem in id_list:
            mapping_list.append(elem - self.global_min_id)

        return origin_list, mapping_list

    def get_id_psi_result(self, intersection_list):
        intersection_result = []
        for elem in intersection_list:
            intersection_result.append(self.global_min_id + elem)

        return intersection_result

    def send_rsa_public_key(self, request, context):
        """
        :param request:
        :param context:
        :return: Process status
        """
        cid = request.cid
        qid = request.qid
        pk_N = request.pk_N
        pk_e = request.pk_e
        # recv_status = False

        if pk_N and pk_e:
            self.rsa_pk = (int(pk_N), pk_e)
            self.rsa_pk_comm_status = True
            print("Public Key received.")
            # print(self.rsa_pk)

        response = tenseal_data_server_pb2.rsa_public_key_response(
            cid=cid,
            qid=qid,
            recv_status=self.rsa_pk_comm_status
        )

        return response

    def send_client_enc_ids(self, request, context):
        """

        :param request:
        :param context:
        :return:
        """
        cid = request.cid
        qid = request.qid
        client_enc_ids_pk_str = request.client_enc_ids_pk_str

        for enc_id_str in client_enc_ids_pk_str:
            self.client_enc_ids_pk.append(int(enc_id_str))

        self.client_enc_ids_comm_status = True
        response = tenseal_data_server_pb2.send_client_enc_ids_response(
            cid=cid,
            qid=qid,
            recv_status=self.client_enc_ids_comm_status
        )

        return response

    def send_server_enc_ids_and_client_dec_ids(self, request, context):
        """

        :param request:
        :param context:
        :return:
        """
        cid = request.cid
        qid = request.qid
        client_dec_ids = request.client_dec_ids
        server_hash_enc_ids = request.server_hash_enc_ids

        for dec_id in client_dec_ids:
            self.client_dec_ids.append(int(dec_id))
        self.client_dec_ids_comm_status = True

        # for hash_enc_id in server_hash_enc_ids:
        self.server_hash_enc_ids = server_hash_enc_ids
        self.server_hash_enc_ids_comm_status = True

        response = tenseal_data_server_pb2.send_server_enc_ids_and_client_dec_ids_response(
            cid=cid,
            qid=qid,
            client_dec_ids_recv_status=self.client_dec_ids_comm_status,
            server_hash_enc_ids_recv_status=self.server_hash_enc_ids_comm_status
        )

        return response
