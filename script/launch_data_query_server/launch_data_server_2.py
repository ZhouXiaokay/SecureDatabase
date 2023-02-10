import sys
import os
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import transmission.tenseal.tenseal_data_server_pb2_grpc as tenseal_data_server_pb2_grpc
from data_query.data_server import DatabaseServer
import grpc
import threading
from transmission.supervise import heart_beat_server
from concurrent import futures
import hydra
from omegaconf import DictConfig
from transmission.psi import id_psi_unencrypted, rsa_psi_encrypted


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
    print("grpc dataServer_2 start...")

    # launch heart-beat sever.
    monitor_server = threading.Thread(target=heart_beat_server, args=(host, port, delay))
    monitor_server.setDaemon(True)
    monitor_server.start()
    # print(threading.enumerate())
    print("monitor server_2 service start... ")

    # ID Psi Debug
    id_list = [5, 7, 9, 10, 12, 10000, 12, 15]
    # intersection_id_list = id_psi_unencrypted(id_list, database_server, options, 2, 2999, 29999, cfg)
    # print(intersection_id_list)

    # RSA Psi Debug
    # rsa_psi_encrypted(id_list, database_server, options, 1, 1999, 19999, cfg)
    status_agg_server = [0, 0, 0, 0, 0, False, '127.0.0.1:50051']
    status_data_server = [0, 0, 0]
    rsa_psi_encrypted(id_list, database_server, options, 1, 1999, status_agg_server, status_data_server, cfg)

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
