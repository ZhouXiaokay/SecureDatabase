import grpc
import transmission.tenseal.tenseal_key_server_pb2 as tenseal_key_server_pb2
import transmission.tenseal.tenseal_key_server_pb2_grpc as tenseal_key_server_pb2_grpc
import transmission.tenseal.tenseal_aggregate_server_pb2 as tenseal_aggregate_server_pb2
import transmission.tenseal.tenseal_aggregate_server_pb2_grpc as tenseal_aggregate_server_pb2_grpc
from transmission.psi.utils import send_rsa_pk, send_client_enc_ids_use_pk, \
    send_server_enc_id_use_sk_and_client_dec_id, get_psi_result
import time


def id_psi_unencrypted(id_list, database_server, options, cid, key_server_qid, agg_server_qid, cfg):
    key_server_address = cfg.servers.key_server.host + ":" + cfg.servers.key_server.port
    aggregate_server_address = cfg.servers.aggregate_server.host + ":" + cfg.servers.aggregate_server.port

    local_max_id, local_min_id = database_server.get_local_max_min_ids(id_list)

    key_server_channel = grpc.insecure_channel(key_server_address, options=options)
    key_server_stub = tenseal_key_server_pb2_grpc.KeyServerServiceStub(key_server_channel)
    request = tenseal_key_server_pb2.get_max_min_ids_request(
        cid=cid,
        qid=key_server_qid,
        max_id=local_max_id,
        min_id=local_min_id
    )
    print("make request to key server.")

    response = key_server_stub.get_global_max_min_id(request)
    print("receive from key server.")

    global_max_id, global_min_id = response.global_max_id, response.global_min_id
    database_server.global_max_id = global_max_id
    database_server.global_min_id = global_min_id
    origin_id_list, mapping_id_list = database_server.get_shuffled_id_list(id_list)
    print("=============")

    aggregate_server_channel = grpc.insecure_channel(aggregate_server_address, options=options)
    aggregate_server_stub = tenseal_aggregate_server_pb2_grpc.AggregateServerServiceStub(aggregate_server_channel)
    request = tenseal_aggregate_server_pb2.intersection_request(
        cid=cid,
        qid=agg_server_qid,
        request_msg=mapping_id_list
    )
    print("make request to aggregate server.")

    response = aggregate_server_stub.get_intersection(request)
    print("receive from aggregate server.")

    intersection_list = response.response_msg
    for index, elem in enumerate(intersection_list):
        intersection_list[index] = elem + global_min_id

    return intersection_list


def rsa_psi_encrypted(id_list, database_server, options, cid, qid, status_agg_server, status_data_server, cfg):
    psi_participator_num = status_agg_server[0]
    total_round = status_agg_server[1]
    current_round = status_agg_server[2]
    participator_index = status_agg_server[3]
    group_index = status_agg_server[4]
    store_psi_result = status_agg_server[5]
    comm_IP = status_agg_server[6]

    # Stage I
    if store_psi_result == False:
        send_rsa_pk(database_server, comm_IP, options, cfg)

    # Waiting for status...
    while not (database_server.rsa_pk_comm_status and database_server.rsa_pk):
        time.sleep(0.1)

    print("RSA public key exchange success.")
    print("================")

    # Stage II
    if store_psi_result == True:
        send_client_enc_ids_use_pk(id_list, database_server, comm_IP, options, cfg)

    while not database_server.client_enc_ids_comm_status:
        time.sleep(0.1)

    print("Exchange encode client ids success.")
    print("================")

    # Stage III
    if store_psi_result == False:
        send_server_enc_id_use_sk_and_client_dec_id(id_list, database_server, comm_IP, options, cfg)

    while not (database_server.client_dec_ids_comm_status and database_server.server_hash_enc_ids_comm_status):
        time.sleep(0.1)

    print("Exchange encode server ids and decode client ids success.")
    print("================")

    # Stage IV
    if store_psi_result == True:
        psi_result = get_psi_result(id_list, database_server.client_dec_ids, database_server.client_ra_list,
                                    database_server.rsa_pk, database_server.server_hash_enc_ids)
        print(psi_result)
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
