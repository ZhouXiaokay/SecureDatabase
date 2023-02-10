import os

import gmpy2
import grpc
import hashlib
import binascii
from Cryptodome.PublicKey import RSA
import transmission.tenseal.tenseal_data_server_pb2_grpc as tenseal_data_server_pb2_grpc
import transmission.tenseal.tenseal_data_server_pb2 as tenseal_data_server_pb2


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


def decode_ids_from_client(enc_ids, sk):
    dec_ids = []
    for enc_id in enc_ids:
        dec_id = gmpy2.powmod(enc_id, sk[1], sk[0])
        dec_ids.append(dec_id)

    return dec_ids


def encode_and_hash_local_id_use_sk(local_ids, sk):
    hash_enc_ids = []
    for id in local_ids:
        hash_id = hash_number(id)
        hash_enc_id = gmpy2.powmod(hash_id, sk[1], sk[0])
        hash_enc_ids.append(hash_number(hash_enc_id))

    return hash_enc_ids


def send_rsa_pk(database_server, comm_IP, options, cfg):
    database_server.rsa_pk, database_server.rsa_sk = generate_rsa_keys()
    client_data_server_channel = grpc.insecure_channel(comm_IP, options=options)
    client_data_server_stub = tenseal_data_server_pb2_grpc.DatabaseServerServiceStub(client_data_server_channel)
    request = tenseal_data_server_pb2.rsa_public_key_request(
        cid=1,
        qid=1,
        pk_N=str(database_server.rsa_pk[0]),
        pk_e=database_server.rsa_pk[1]
    )
    print("Sending PSI key...")

    response = client_data_server_stub.send_rsa_public_key(request)
    if not response.recv_status:
        print("Failed.")
    else:
        database_server.rsa_pk_comm_status = True


def send_client_enc_ids_use_pk(local_ids, database_server, comm_IP, options, cfg):
    server_data_server_channel = grpc.insecure_channel(comm_IP, options=options)
    server_data_server_stub = tenseal_data_server_pb2_grpc.DatabaseServerServiceStub(server_data_server_channel)

    database_server.client_enc_ids_pk, database_server.client_ra_list = encode_local_id_use_pk(local_ids,
                                                                                               database_server.rsa_pk)

    client_enc_ids_str = []
    for enc_id in database_server.client_enc_ids_pk:
        client_enc_ids_str.append(str(enc_id))

    request = tenseal_data_server_pb2.send_client_enc_ids_request(
        cid=1,
        qid=1,
        client_enc_ids_pk_str=client_enc_ids_str
    )
    print("Sending encrypted client ids...")

    response = server_data_server_stub.send_client_enc_ids(request)
    if not response.recv_status:
        print("Failed.")
    else:
        database_server.client_enc_ids_comm_status = True
