import transmission.teanseal.tenseal_data_pb2_grpc as tenseal_data_pb2_grpc
import transmission.teanseal.tenseal_data_pb2 as tenseal_data_pb2

import transmission.request.request_data_pb2 as request_data_pb2
import transmission.request.request_data_pb2_grpc as request_data_pb2_grpc
import tenseal as ts
import grpc


def getMaxValue(pk_ctx):
    max_msg_size = 1000000000
    options = [('grpc.max_send_message_length', max_msg_size),
               ('grpc.max_receive_message_length', max_msg_size)]
    channel = grpc.insecure_channel('127.0.0.1:50052', options=options)
    stub = tenseal_data_pb2_grpc.SafeTransmissionStub(channel)

    request = tenseal_data_pb2.requestOP(id="", op="")
    response = stub.MaxValue(request)
    enc_vector = ts.ckks_vector_from(pk_ctx, response.msg)
    return enc_vector


def getMinValue(pk_ctx):
    max_msg_size = 1000000000
    options = [('grpc.max_send_message_length', max_msg_size),
               ('grpc.max_receive_message_length', max_msg_size)]
    channel = grpc.insecure_channel('127.0.0.1:50052', options=options)
    stub = tenseal_data_pb2_grpc.SafeTransmissionStub(channel)

    request = tenseal_data_pb2.requestOP(id="", op="")
    response = stub.MinValue(request)
    enc_vector = ts.ckks_vector_from(pk_ctx, response.msg)
    return enc_vector

def getSumValue(pk_ctx):
    max_msg_size = 1000000000
    options = [('grpc.max_send_message_length', max_msg_size),
               ('grpc.max_receive_message_length', max_msg_size)]
    channel = grpc.insecure_channel('127.0.0.1:50052', options=options)
    stub = tenseal_data_pb2_grpc.SafeTransmissionStub(channel)

    request = tenseal_data_pb2.requestOP(id="", op="")
    response = stub.SumValue(request)
    enc_vector = ts.ckks_vector_from(pk_ctx, response.msg)
    return enc_vector

def getAddMaxValue(pk_ctx):
    max_msg_size = 1000000000
    options = [('grpc.max_send_message_length', max_msg_size),
               ('grpc.max_receive_message_length', max_msg_size)]
    channel = grpc.insecure_channel('127.0.0.1:50052', options=options)
    stub = tenseal_data_pb2_grpc.SafeTransmissionStub(channel)
    request = tenseal_data_pb2.requestOP(id="", op="")
    response = stub.MaxValue(request)
    enc_vector_1 = ts.ckks_vector_from(pk_ctx, response.msg)

    channel = grpc.insecure_channel('127.0.0.1:50053', options=options)
    stub = tenseal_data_pb2_grpc.SafeTransmissionStub(channel)
    request = tenseal_data_pb2.requestOP(id="", op="")
    response = stub.MaxValue(request)
    enc_vector_2 = ts.ckks_vector_from(pk_ctx, response.msg)

    enc_vector = enc_vector_1 + enc_vector_2

    return enc_vector

def getAddSumValue(pk_ctx):
    max_msg_size = 1000000000
    options = [('grpc.max_send_message_length', max_msg_size),
               ('grpc.max_receive_message_length', max_msg_size)]
    channel = grpc.insecure_channel('127.0.0.1:50052', options=options)
    stub = tenseal_data_pb2_grpc.SafeTransmissionStub(channel)
    request = tenseal_data_pb2.requestOP(id="", op="")
    response = stub.SumValue(request)
    enc_vector_1 = ts.ckks_vector_from(pk_ctx, response.msg)

    channel = grpc.insecure_channel('127.0.0.1:50053', options=options)
    stub = tenseal_data_pb2_grpc.SafeTransmissionStub(channel)
    request = tenseal_data_pb2.requestOP(id="", op="")
    response = stub.SumValue(request)
    enc_vector_2 = ts.ckks_vector_from(pk_ctx, response.msg)

    enc_vector = enc_vector_1 + enc_vector_2

    return enc_vector

"""
input: encrypted vector
return: decrypted vector
process: send request to KeyServer
"""
def resultsDecrypt(enc_vector):
    max_msg_size = 1000000000
    options = [('grpc.max_send_message_length', max_msg_size),
               ('grpc.max_receive_message_length', max_msg_size)]
    channel = grpc.insecure_channel('127.0.0.1:50054', options=options)
    stub = request_data_pb2_grpc.RequestTransmissionStub(channel)

    serialize_msg = enc_vector.serialize()
    request = request_data_pb2.results(msg=serialize_msg)
    response = stub.RequestDecrypt(request)

    results = response.msg

    return results
