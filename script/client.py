import transmission.request.request_data_pb2 as request_data_pb2
import transmission.request.request_data_pb2_grpc as request_data_pb2_grpc

import tenseal as ts
import grpc
import pickle


def sendRequest(op):
    max_msg_size = 1000000000
    options = [('grpc.max_send_message_length', max_msg_size),
               ('grpc.max_receive_message_length', max_msg_size)]
    channel = grpc.insecure_channel('127.0.0.1:50051', options=options)
    stub = request_data_pb2_grpc.RequestTransmissionStub(channel)

    request = request_data_pb2.requestQuery(id="", op=op)
    response = stub.RequestParsing(request)

    results = pickle.loads(response.msg)

    return results


if __name__ == "__main__":
    op = "max"
    maxResult = sendRequest(op)
    print(maxResult)
    op = "min"
    minResult = sendRequest(op)
    print(minResult)
    op = "sum"
    sumResult = sendRequest(op)
    print(sumResult)
    op = "addsum"
    addResult = sendRequest(op)
    print(addResult)
