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
from transmission.psi import id_psi_unencrypted, init_data_server_status, rsa_psi_encrypted
from transmission.psi.utils import get_agg_server_status


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
    id_list = [x for x in range(2, 50)]
    # intersection_id_list = id_psi_unencrypted(id_list, database_server, options, 2, 2999, 29999, cfg)
    # print(intersection_id_list)

    # RSA Psi Debug
    # rsa_psi_encrypted(id_list, database_server, options, 1, 1999, 19999, cfg)
    # status_agg_server = [0, 0, 1, 0, 0, False, '127.0.0.1:50051']
    # status_data_server = ['127.0.0.1:50052', True, 0]
    print(database_server.data_server_status)
    init_data_server_status(database_server, '127.0.0.1:50052')
    print(database_server.data_server_status)
    get_agg_server_status(database_server.data_server_status, 2, 2999, options, cfg)

    # rsa_psi_encrypted(id_list, database_server, options, 2, 2999, status_agg_server, cfg)
    # print(database_server.data_server_status)

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
