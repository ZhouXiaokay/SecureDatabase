import grpc
import transmission.tenseal.tenseal_key_server_pb2 as tenseal_key_server_pb2
import transmission.tenseal.tenseal_key_server_pb2_grpc as tenseal_key_server_pb2_grpc
import transmission.tenseal.tenseal_aggregate_server_pb2 as tenseal_aggregate_server_pb2
import transmission.tenseal.tenseal_aggregate_server_pb2_grpc as tenseal_aggregate_server_pb2_grpc


def id_psi_unencrypted(id_list, database_server, options, cid, key_server_qid, agg_server_qid, cfg):
    key_server_channel = cfg.servers.key_server.host + ":" + cfg.servers.key_server.port
    aggregate_server_channel = cfg.servers.aggregate_server.host + ":" + cfg.servers.aggregate_server.port

    local_max_id, local_min_id = database_server.get_local_max_min_ids(id_list)

    key_server_channel = grpc.insecure_channel(key_server_channel, options=options)
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

    aggregate_server_channel = grpc.insecure_channel(aggregate_server_channel, options=options)
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
