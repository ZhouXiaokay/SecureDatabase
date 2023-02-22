import time

import grpc
import tenseal as ts
import transmission.tenseal.tenseal_key_server_pb2 as tenseal_key_server_pb2
import transmission.tenseal.tenseal_key_server_pb2_grpc as tenseal_key_server_pb2_grpc
import transmission.tenseal.tenseal_aggregate_server_pb2 as tenseal_aggregate_server_pb2
import transmission.tenseal.tenseal_aggregate_server_pb2_grpc as tenseal_aggregate_server_pb2_grpc
from transmission.psi.utils import get_agg_server_status, init_data_server_status, \
    get_final_psi_result, rsa_double_psi_encrypted


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


def rsa_psi(database_server, id_list, local_IP, cid, qid, he_context_path, options, cfg):
    start_time = time.time()
    psi_id_list = id_list
    psi_result_status = [False, bytes("None", 'utf-8')]
    init_data_server_status(database_server, local_IP)
    while True:
        agg_server_response = get_agg_server_status(database_server.data_server_status,
                                                    cid, qid, psi_result_status, options, cfg)
        if agg_server_response[1] == True:
            he_context_bytes = open(he_context_path, "rb").read()
            he_context = ts.context_from(he_context_bytes)
            psi_enc_result = ts.ckks_vector_from(he_context, agg_server_response[2])
            psi_dec_result = psi_enc_result.decrypt()
            psi_result = get_final_psi_result(psi_dec_result)
            database_server.reset_all_rsa_psi_status()
            print("RSA-PSI Finished.")
            end_time = time.time()
            print(f"Total time: {end_time - start_time - 8}")
            return psi_result

        psi_id_list, psi_result_status = rsa_double_psi_encrypted(psi_id_list, database_server, cid, qid,
                                                                  agg_server_response[0], he_context_path,
                                                                  options, cfg)