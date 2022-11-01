import os
import sys
import transmission.tenseal.tenseal_client_proxy_pb2 as tenseal_client_proxy_pb2
import transmission.tenseal.tenseal_client_proxy_pb2_grpc as tenseal_client_proxy_pb2_grpc
import grpc
import pickle
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))



def sendRequest():
    max_msg_size = 1000000000
    options = [('grpc.max_send_message_length', max_msg_size),
               ('grpc.max_receive_message_length', max_msg_size)]
    channel = grpc.insecure_channel('127.0.0.1:50060', options=options)
    stub = tenseal_client_proxy_pb2_grpc.ClientProxyServiceStub(channel)

    request = tenseal_client_proxy_pb2.query_msg_client(cid=1, qid=3457, db_name="database_1", column_name="value_1",
                                                        op="max",
                                                        table_name="table_1")
    response = stub.data_query(request)
    result = pickle.loads(response.dec_result)
    print(result)


if __name__ == "__main__":
    sendRequest()
