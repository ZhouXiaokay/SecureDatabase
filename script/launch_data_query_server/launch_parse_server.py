import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import hydra
from omegaconf import DictConfig
from data_query.parse_server import ParseServer
from concurrent import futures
import grpc
import threading
from transmission.supervise import heart_beat_client
import transmission.tenseal.tenseal_parse_server_pb2_grpc as tenseal_parse_server_pb2_grpc


def launch_parse_server(host, port, delay, address_dict):
    parseServer_address = host + ":" + str(port)
    max_msg_size = 1000000000
    pk_ctx_file = "../../transmission/ts_ckks_pk.config"
    options = [('grpc.max_send_message_length', max_msg_size), ('grpc.max_receive_message_length', max_msg_size)]
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5), options=options)
    tenseal_parse_server_pb2_grpc.add_ParseServerServiceServicer_to_server(ParseServer(address_dict, pk_ctx_file),
                                                                           server)
    server.add_insecure_port(parseServer_address)
    server.start()
    print("grpc parse_server start...")

    # launch heart-beat client
    for index, value in enumerate(address_dict.values()):
        server_host, server_port = value.split(':')
        monitor_client = threading.Thread(target=heart_beat_client, args=(server_host, int(server_port), delay))
        monitor_client.setDaemon(True)
        monitor_client.start()
        print(f"monitor client {index + 1} service start... ")

    server.wait_for_termination()


@hydra.main(version_base=None, config_path="../../conf", config_name="conf")
def main(cfg: DictConfig):
    host = cfg.servers.parse_server.host
    port = int(cfg.servers.parse_server.port)
    delay = cfg.defs.parse_server_delay
    address_dict = {"DATABASE_1": cfg.servers.data_server_1.host + ':' + cfg.servers.data_server_1.port,
                    "DATABASE_2": cfg.servers.data_server_2.host + ':' + cfg.servers.data_server_2.port,
                    "DATABASE_3": cfg.servers.data_server_3.host + ':' + cfg.servers.data_server_3.port,
                    "KEYSERVER": cfg.servers.key_server.host + ':' + cfg.servers.key_server.port,
                    "CLIENTPROXY": cfg.servers.client_proxy.host + ':' + cfg.servers.client_proxy.port}
    launch_parse_server(host, port, delay, address_dict)


if __name__ == '__main__':
    main()
