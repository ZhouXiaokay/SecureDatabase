import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import hydra
from omegaconf import DictConfig
from data_modeling import AggregateServer
import transmission.tenseal.tenseal_aggregate_server_pb2_grpc as tenseal_aggregate_server_pb2_grpc
import grpc
from concurrent import futures
from data_modeling.model import Logistic,Linear,DNN
from conf import args_parser


def launch_aggregate_server(host, port):
    args = args_parser()
    aggr_server_address = host + ":" + str(port)
    max_msg_size = 1000000000
    pk_ctx_file = "../../transmission/ts_ckks_pk.config"
    options = [('grpc.max_send_message_length', max_msg_size), ('grpc.max_receive_message_length', max_msg_size)]
    model = DNN(n_f=args.n_features)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5), options=options)
    tenseal_aggregate_server_pb2_grpc.add_AggregateServerServiceServicer_to_server(
        AggregateServer(3, pk_ctx_file, model),
        server)
    server.add_insecure_port(aggr_server_address)
    server.start()
    print("Aggregate Server start")
    server.wait_for_termination()


@hydra.main(version_base=None, config_path="../../conf", config_name="conf")
def main(cfg: DictConfig):
    host = cfg.servers.aggregate_server.host
    port = int(cfg.servers.aggregate_server.port)
    launch_aggregate_server(host, port)


if __name__ == '__main__':
    main()