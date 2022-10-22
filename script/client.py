import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import transmission.request.request_clientProxy_pb2 as request_clientProxy_pb2
import transmission.request.request_clientProxy_pb2_grpc as request_clientProxy_pb2_grpc

import tenseal as ts
import grpc
import pickle


def sendRequest():
    max_msg_size = 1000000000
    options = [('grpc.max_send_message_length', max_msg_size),
               ('grpc.max_receive_message_length', max_msg_size)]
    channel = grpc.insecure_channel('127.0.0.1:50060', options=options)
    stub = request_clientProxy_pb2_grpc.ClientProxyServiceStub(channel)

    request = request_clientProxy_pb2.requestProxy(cid=1, qid=3457, db_name="total", column_name="value_1",
                                                   op="count",
                                                   table_name="table_1")
    response = stub.RequestProxy(request)
    result = pickle.loads(response.result)
    print(result)


if __name__ == "__main__":
    sendRequest()
