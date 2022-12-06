import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import transmission.tenseal.tenseal_data_server_pb2_grpc as tenseal_data_server_pb2_grpc
from data_query.data_server import DatabaseServer
import grpc
import threading
from transmission.supervise import heart_beat_server
from concurrent import futures
import hydra
from omegaconf import DictConfig
import transmission.tenseal.tenseal_key_server_pb2 as tenseal_key_server_pb2
import transmission.tenseal.tenseal_key_server_pb2_grpc as tenseal_key_server_pb2_grpc


def launch_data_server(host, port, delay, name, cfg):
    dataServer_address = host + ":" + str(port)
    max_msg_size = 1000000000
    pk_file = "../../transmission/ts_ckks_pk.config"
    options = [('grpc.max_send_message_length', max_msg_size), ('grpc.max_receive_message_length', max_msg_size)]
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5), options=options)

    database_server = DatabaseServer(dataServer_address, pk_file, name, cfg)
    tenseal_data_server_pb2_grpc.add_DatabaseServerServiceServicer_to_server(
        database_server,
        server)
    # Old version
    # tenseal_data_server_pb2_grpc.add_DatabaseServerServiceServicer_to_server(
    #     DatabaseServer(dataServer_address, pk_file, name, cfg),
    #     server)

    server.add_insecure_port(dataServer_address)
    server.start()
    print("grpc dataServer_1 start...")

    # launch heart-beat sever.
    monitor_server = threading.Thread(target=heart_beat_server, args=(host, port, delay))
    monitor_server.setDaemon(True)
    monitor_server.start()
    # print(threading.enumerate())
    print("monitor server_1 service start... ")

    # ID Psi Debug
    id_list = [5, 7, 9, 10, 12, 10000]
    local_max_id, local_min_id = database_server.get_local_max_min_ids(id_list)

    channel = grpc.insecure_channel('127.0.0.1:50070', options=options)
    stub = tenseal_key_server_pb2_grpc.KeyServerServiceStub(channel)
    request = tenseal_key_server_pb2.get_max_min_ids_request(
        cid=2,
        qid=2999,
        max_id=local_max_id,
        min_id=local_min_id
    )
    print("make request.")

    response = stub.get_global_max_min_id(request)
    print("receive")

    global_max_id, global_min_id = response.global_max_id, response.global_min_id
    print(global_max_id, global_min_id)

    database_server.global_max_id = global_max_id
    database_server.global_min_id = global_min_id
    origin_id_list, mapping_id_list = database_server.get_shuffled_id_list(id_list)
    print(mapping_id_list)
    #####

    server.wait_for_termination()


@hydra.main(version_base=None, config_path="../../conf", config_name="conf")
def main(cfg: DictConfig):
    host = cfg.servers.data_server_2.host
    port = int(cfg.servers.data_server_2.port)
    delay = cfg.defs.delay
    name = cfg.servers.data_server_2.name
    launch_data_server(host, port, delay, name, cfg)


if __name__ == '__main__':
    main()
