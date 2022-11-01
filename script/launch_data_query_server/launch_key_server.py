import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import threading
import hydra
from omegaconf import DictConfig
from data_query.key_server import KeyServer
import transmission.tenseal.tenseal_key_server_pb2_grpc as tenseal_key_server_pb2_grpc
import grpc
from transmission.supervise import heart_beat_server
from concurrent import futures



def launch_key_server(host, port, delay):
    keyServer_address = host + ":" + str(port)
    max_msg_size = 1000000000
    sk_ctx_file = "../../transmission/ts_ckks.config"
    options = [('grpc.max_send_message_length', max_msg_size), ('grpc.max_receive_message_length', max_msg_size)]
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5), options=options)
    tenseal_key_server_pb2_grpc.add_KeyServerServiceServicer_to_server(KeyServer(sk_ctx_file), server)
    server.add_insecure_port(keyServer_address)

    server.start()
    print("grpc key_server start...")
    # launch heart-beat sever.
    monitor_server = threading.Thread(target=heart_beat_server, args=(host, port, delay))
    monitor_server.setDaemon(True)
    monitor_server.start()
    # print(threading.enumerate())
    print("monitor keyserver service start... ")

    server.wait_for_termination()


@hydra.main(version_base=None, config_path="../../conf", config_name="conf")
def main(cfg: DictConfig):
    host = cfg.servers.key_server.host
    port = int(cfg.servers.key_server.port)
    delay = cfg.defs.delay
    launch_key_server(host, port, delay)


if __name__ == '__main__':
    main()
