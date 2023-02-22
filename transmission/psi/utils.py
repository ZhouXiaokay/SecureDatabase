import os
import time
import random
import gmpy2
import grpc
import hashlib
import binascii
import tenseal as ts
from Cryptodome.PublicKey import RSA
from distutils.util import strtobool
import transmission.tenseal.tenseal_data_server_pb2_grpc as tenseal_data_server_pb2_grpc
import transmission.tenseal.tenseal_data_server_pb2 as tenseal_data_server_pb2
import transmission.tenseal.tenseal_aggregate_server_pb2 as tenseal_aggregate_server_pb2
import transmission.tenseal.tenseal_aggregate_server_pb2_grpc as tenseal_aggregate_server_pb2_grpc


def generate_rsa_keys():
    """

    :return: RSA's public key and secret key
    """
    key = RSA.generate(1024)
    pk = (key.n, key.e)
    sk = (key.n, key.d)
    return pk, sk


def hash_number(number):
    """

    :param number: unhashed number
    :return:hashed number
    """
    hash_obj = hashlib.sha1(str(number).encode('utf-8'))
    digest_hex = hash_obj.hexdigest()
    return int(digest_hex, 16)


def encode_local_id_use_pk(local_ids, pk):
    """

    :param local_ids:
    :param pk: public key
    :return: encrypted id list and random number list
    """
    enc_ids = []
    ra_list = []
    for id in local_ids:
        hash_id = hash_number(id)
        hash_enc_id = hash_id % pk[0]

        # generate random number ra
        ra = int(binascii.hexlify(os.urandom(128)), 16)
        ra_enc = gmpy2.powmod(ra, pk[1], pk[0])
        ra_list.append(ra)
        enc_ids.append(int(hash_enc_id * ra_enc))  # invert mpz to int

    return enc_ids, ra_list


def decode_ids(enc_ids, sk):
    dec_ids = []
    for enc_id in enc_ids:
        dec_id = gmpy2.powmod(enc_id, sk[1], sk[0])
        dec_ids.append(int(dec_id))

    return dec_ids


def encode_and_hash_local_ids_use_sk(local_ids, sk):
    hash_enc_ids = []
    for id in local_ids:
        hash_id = hash_number(id)
        hash_enc_id = gmpy2.powmod(hash_id, sk[1], sk[0])
        hash_enc_ids.append(hash_number(hash_enc_id))

    return hash_enc_ids


def invert_and_hash_decode_ids(decode_ids, ra_list, pk):
    hash_ids = []
    for dec_id, ra in zip(decode_ids, ra_list):
        ra_inv = gmpy2.invert(ra, pk[0])
        hash_ids.append(hash_number((dec_id * ra_inv) % pk[0]))

    return hash_ids


def get_psi_index(client_hash_ids, server_hash_ids):
    psi_index = []
    for i in range(len(client_hash_ids)):
        client_hash_id = client_hash_ids[i]
        for server_hash_id in server_hash_ids:
            if client_hash_id == server_hash_id:
                psi_index.append(i)

    return psi_index


def get_double_psi_result(local_ids, decode_ids, ra_list, pk, server_hash_ids):
    client_hash_ids = invert_and_hash_decode_ids(decode_ids, ra_list, pk)
    psi_index = get_psi_index(client_hash_ids, server_hash_ids)
    psi_result = []
    for index in psi_index:
        psi_result.append(local_ids[index])

    return psi_result


def encode_empty_psi_result():
    value = random.randint(1, 10)
    length = random.randint(2, 10)
    return [value for _ in range(length)]


def get_final_psi_result(psi_dec_result):
    psi_round_result = []
    for item in psi_dec_result:
        psi_round_result.append(round(item))
    psi_result = set(psi_round_result)
    if len(psi_result) != len(psi_dec_result):
        return []

    return psi_round_result


def init_data_server_status(database_server, local_IP):
    database_server.data_server_status = [local_IP, True, 0]


def update_data_server_status(data_server_status, store_psi_result, current_round):
    data_server_status[1] = store_psi_result
    data_server_status[2] = current_round


def get_agg_server_status(data_server_status, cid, qid, psi_result_status, options, cfg):
    print(data_server_status)
    data_server_status_str = []
    carry_psi_final_result = psi_result_status[0]
    psi_final_result = psi_result_status[1].serialize() if carry_psi_final_result \
        else psi_result_status[1]

    for item in data_server_status:
        data_server_status_str.append(str(item))

    agg_server_address = cfg.servers.aggregate_server.host + ":" + cfg.servers.aggregate_server.port
    agg_server_channel = grpc.insecure_channel(agg_server_address, options=options)
    agg_server_stub = tenseal_aggregate_server_pb2_grpc.AggregateServerServiceStub(agg_server_channel)

    request = tenseal_aggregate_server_pb2.data_server_status_request(
        cid=cid,
        qid=qid,
        data_server_status=data_server_status_str,
        carry_psi_final_result=psi_result_status[0],
        psi_final_result=psi_final_result
    )
    print("Request for AggServer status...")

    response = agg_server_stub.get_agg_server_status(request)
    agg_server_status = response.agg_server_status
    # print(agg_server_status)

    if response.carry_psi_final_result == True:
        return [agg_server_status, True, response.psi_final_result]
    else:
        return [agg_server_status, False, None]


def send_rsa_pk(database_server, cid, qid, comm_IP, options, cfg):
    database_server.rsa_pk, database_server.rsa_sk = generate_rsa_keys()
    client_data_server_channel = grpc.insecure_channel(comm_IP, options=options)
    client_data_server_stub = tenseal_data_server_pb2_grpc.DatabaseServerServiceStub(client_data_server_channel)
    request = tenseal_data_server_pb2.rsa_public_key_request(
        cid=cid,
        qid=qid,
        pk_N=str(database_server.rsa_pk[0]),
        pk_e=database_server.rsa_pk[1]
    )
    print("Sending PSI key...")

    response = client_data_server_stub.send_rsa_public_key(request)
    if not response.recv_status:
        print("Failed.")
    else:
        database_server.rsa_pk_comm_status = True


def send_client_enc_ids_use_pk(local_ids, database_server, cid, qid, comm_IP, options, cfg):
    server_data_server_channel = grpc.insecure_channel(comm_IP, options=options)
    server_data_server_stub = tenseal_data_server_pb2_grpc.DatabaseServerServiceStub(server_data_server_channel)

    database_server.client_enc_ids_pk, database_server.client_ra_list = encode_local_id_use_pk(local_ids,
                                                                                               database_server.rsa_pk)

    client_enc_ids_str = []
    for enc_id in database_server.client_enc_ids_pk:
        client_enc_ids_str.append(str(enc_id))

    request = tenseal_data_server_pb2.send_client_enc_ids_request(
        cid=cid,
        qid=qid,
        client_enc_ids_pk_str=client_enc_ids_str
    )
    print("Sending encrypted client ids...")

    response = server_data_server_stub.send_client_enc_ids(request)
    if not response.recv_status:
        print("Failed.")
    else:
        database_server.client_enc_ids_comm_status = True


def send_server_enc_id_use_sk_and_client_dec_id(local_ids, database_server, cid, qid, comm_IP, options, cfg):
    client_data_server_channel = grpc.insecure_channel(comm_IP, options=options)
    client_data_server_stub = tenseal_data_server_pb2_grpc.DatabaseServerServiceStub(client_data_server_channel)

    database_server.client_dec_ids = decode_ids(database_server.client_enc_ids_pk, database_server.rsa_sk)
    database_server.server_hash_enc_ids = encode_and_hash_local_ids_use_sk(local_ids, database_server.rsa_sk)

    client_dec_ids_str = []
    for dec_id in database_server.client_dec_ids:
        client_dec_ids_str.append(str(dec_id))

    server_hash_enc_ids_str = []
    for hash_enc_id in database_server.server_hash_enc_ids:
        server_hash_enc_ids_str.append(str(hash_enc_id))

    request = tenseal_data_server_pb2.send_server_enc_ids_and_client_dec_ids_request(
        cid=cid,
        qid=qid,
        client_dec_ids=client_dec_ids_str,
        server_hash_enc_ids=server_hash_enc_ids_str
    )
    print("Sending encrypted server ids and decrypted client ids...")

    response = client_data_server_stub.send_server_enc_ids_and_client_dec_ids(request)
    if not (response.client_dec_ids_recv_status and response.server_hash_enc_ids_recv_status):
        print("Failed.")
    else:
        database_server.client_dec_ids_comm_status = True
        database_server.server_hash_enc_ids_comm_status = True


def rsa_double_psi_encrypted(id_list, database_server, cid, qid, agg_server_status,
                             he_context_path, options, cfg):
    psi_participator_num = int(agg_server_status[0])
    total_rounds = int(agg_server_status[1])
    current_round = int(agg_server_status[2])
    participator_index = int(agg_server_status[3])
    group_index = int(agg_server_status[4])
    store_psi_result = True if strtobool(agg_server_status[5]) else False
    comm_IP = agg_server_status[6]
    carry_final_psi_result = False
    psi_final_result = bytes("None", 'utf-8')

    if comm_IP != '0':
        # Stage I
        if store_psi_result == False:
            send_rsa_pk(database_server, cid, qid, comm_IP, options, cfg)

        # Waiting for status...
        while not (database_server.rsa_pk_comm_status and database_server.rsa_pk):
            time.sleep(0.1)

        print("RSA public key exchange success.")
        print("================")

        # Stage II
        if store_psi_result == True:
            send_client_enc_ids_use_pk(id_list, database_server, cid, qid, comm_IP, options, cfg)

        while not database_server.client_enc_ids_comm_status:
            time.sleep(0.1)

        print("Exchange encode client ids success.")
        print("================")

        # Stage III
        if store_psi_result == False:
            send_server_enc_id_use_sk_and_client_dec_id(id_list, database_server, cid, qid,
                                                        comm_IP, options, cfg)

        while not (database_server.client_dec_ids_comm_status and database_server.server_hash_enc_ids_comm_status):
            time.sleep(0.1)

        print("Exchange encode server ids and decode client ids success.")
        print("================")

        # Stage IV
        if store_psi_result == True:
            database_server.psi_result = get_double_psi_result(id_list, database_server.client_dec_ids,
                                                               database_server.client_ra_list,
                                                               database_server.rsa_pk,
                                                               database_server.server_hash_enc_ids)
            # print(database_server.psi_result)
            if current_round == total_rounds:
                he_context_bytes = open(he_context_path, "rb").read()
                he_context = ts.context_from(he_context_bytes)
                if len(database_server.psi_result) == 0:
                    database_server.psi_result = encode_empty_psi_result()
                psi_final_result = ts.ckks_vector(he_context, database_server.psi_result)
                carry_final_psi_result = True
        else:
            pass
    else:
        if store_psi_result == True:
            database_server.psi_result = id_list
        else:
            pass
    # print("Double PSI process done.")
    # print("Public key: ", database_server.rsa_pk)
    # print("================")
    # print("Private key: ",database_server.rsa_sk)
    # print("================")
    # print("Random number list: ", database_server.client_ra_list)
    # print("================")
    # print("Client_enc_ids_pk: ", database_server.client_enc_ids_pk)
    # print("================")
    # print("Client_dec_ids: ", database_server.client_dec_ids)
    # print("================")
    # print("Server_hash_enc_ids: ", database_server.server_hash_enc_ids)
    # print("================")
    # print("PSI_result: ", database_server.psi_result)

    # Update local status
    update_data_server_status(database_server.data_server_status, store_psi_result, current_round)
    database_server.reset_rsa_psi_status_per_round()
    return database_server.psi_result, [carry_final_psi_result, psi_final_result]
