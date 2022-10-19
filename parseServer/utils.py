import transmission.tenseal.tenseal_data_pb2_grpc as tenseal_data_pb2_grpc
import transmission.tenseal.tenseal_data_pb2 as tenseal_data_pb2

import transmission.request.request_keyServer_pb2 as request_keyServer_pb2
import transmission.request.request_keyServer_pb2_grpc as request_keyServer_pb2_grpc

import tenseal as ts
import grpc
import pickle

# establish connection with dataServer_dbname,return stub
def get_db_stub(db_name, address_dict, options):
    db_name = db_name.upper()

    address = address_dict[db_name]
    channel = grpc.insecure_channel(address, options=options)
    stub = tenseal_data_pb2_grpc.DatabaseServerServiceStub(channel)
    return stub


# establish connection with keyServer
def get_keyserver_stub(address_dict, options):
    address = address_dict["KEYSERVER"]
    channel = grpc.insecure_channel(address, options=options)
    stub = request_keyServer_pb2_grpc.KeyServerServiceStub(channel)

    return stub


# establish all connection with dataServer and return the list
def get_all_db_stub(address_dict, options):
    stub_list = []
    for key in address_dict:
        if key.upper() != "KEYSERVER":
            address = address_dict[key]
            channel = grpc.insecure_channel(address, options=options)
            stub = tenseal_data_pb2_grpc.DatabaseServerServiceStub(channel)
            stub_list.append(stub)
    return stub_list


"""
input: encrypted vector
return: decrypted vector
process: send request to KeyServer
"""


# send the encrypted result to keyServer
def return_results(key_server_stub, enc_vector, proxy_request):
    serialize_msg = enc_vector.serialize()
    request = request_keyServer_pb2.requestEncResult(cid=proxy_request.cid, qid=proxy_request.qid,
                                                     ipaddress=proxy_request.ipaddress, encResult=serialize_msg)
    response = key_server_stub.ReturnResult(request)


def decrypt_results(key_server_stub, enc_vector):
    enc_serialize_msg = enc_vector.serialize()
    request = request_keyServer_pb2.vectorResult(vectorMsg = enc_serialize_msg)
    response = key_server_stub.RequestDecrypt(request)
    dec_serialize_msg = response.vectorMsg
    dec_vector = pickle.loads(dec_serialize_msg)
    return dec_vector