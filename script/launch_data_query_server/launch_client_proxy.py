import sys
import os
from data_query.client_proxy import ClientProxy
from concurrent import futures
import grpc

import transmission.tenseal.tenseal_client_proxy_pb2_grpc as tenseal_client_proxy_pb2_grpc
import hydra
from omegaconf import DictConfig

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@hydra.main(version_base=None, config_path="../../conf", config_name="conf")
def launch_client_proxy(cfg: DictConfig):
    max_msg_size = 1000000000
    options = [('grpc.max_send_message_length', max_msg_size), ('grpc.max_receive_message_length', max_msg_size)]
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5), options=options)
    tenseal_client_proxy_pb2_grpc.add_ClientProxyServiceServicer_to_server(
        ClientProxy(cfg.servers.parse_server.host + ':' + cfg.servers.parse_server.port,
                    cfg.servers.client_proxy.host + ':' + cfg.servers.client_proxy.port), server)
    server.add_insecure_port(cfg.servers.client_proxy.host + ':' + cfg.servers.client_proxy.port)
    server.start()
    print("grpc client_proxy start...")
    server.wait_for_termination()


if __name__ == '__main__':
    launch_client_proxy()
