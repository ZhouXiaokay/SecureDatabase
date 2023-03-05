import transmission.tenseal.tenseal_data_server_pb2_grpc as tenseal_data_server_pb2_grpc
import transmission.tenseal.tenseal_data_server_pb2 as tenseal_data_server_pb2

import transmission.tenseal.tenseal_key_server_pb2 as tenseal_key_server_pb2
import transmission.tenseal.tenseal_key_server_pb2_grpc as tenseal_key_server_pb2_grpc
import grpc


# establish connection with dataServer_dbname,return stub
def get_db_stub(db_name, address_dict, options):
    db_name = db_name.upper()

    address = address_dict[db_name]
    channel = grpc.insecure_channel(address, options=options)
    stub = tenseal_data_server_pb2_grpc.DatabaseServerServiceStub(channel)
    return stub


# establish connection with key_server
def get_key_server_stub(address_dict, options):
    address = address_dict["KEYSERVER"]
    channel = grpc.insecure_channel(address, options=options)
    stub = tenseal_key_server_pb2_grpc.KeyServerServiceStub(channel)

    return stub


# establish all connection with dataServer and return the list
def get_all_db_stub(address_dict, options):
    stub_list = []
    for key in address_dict:
        if "DATA" in key.upper():
            address = address_dict[key]
            channel = grpc.insecure_channel(address, options=options)
            stub = tenseal_data_server_pb2_grpc.DatabaseServerServiceStub(channel)
            stub_list.append(stub)
    return stub_list


"""
input: encrypted vector
return: decrypted vector
process: send request to KeyServer
"""


# send the encrypted result to key_server
def return_results(key_server_stub, enc_vector, proxy_request):
    serialize_msg = enc_vector.serialize()
    request = tenseal_key_server_pb2.query_result_parse_server(cid=proxy_request.cid, qid=proxy_request.qid,
                                                               ip_address=proxy_request.ip_address,
                                                               enc_result=serialize_msg)
    key_server_stub.return_enc_query_result(request)
