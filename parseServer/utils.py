import transmission.tenseal.tenseal_data_pb2_grpc as tenseal_data_pb2_grpc
import transmission.tenseal.tenseal_data_pb2 as tenseal_data_pb2

import transmission.request.request_keyServer_pb2 as request_keyServer_pb2
import transmission.request.request_keyServer_pb2_grpc as request_keyServer_pb2_grpc

import tenseal as ts
import grpc


# initialize stub with all dataServer
def getStubDict(address_dict, options):
    stubDict = {}
    for key in address_dict:
        if key.upper() == "KEYSERVER":
            address = address_dict[key]
            channel = grpc.insecure_channel(address, options=options)
            stub = request_keyServer_pb2_grpc.KeyServerServiceStub(channel)
            key = key.upper()
            stubDict[key] = stub
        else:
            address = address_dict[key]
            channel = grpc.insecure_channel(address, options=options)
            stub = tenseal_data_pb2_grpc.DatabaseServerServiceStub(channel)
            key = key.upper()
            stubDict[key] = stub

    return stubDict


def getDBStub(db_name, address_dict, options):
    db_name = db_name.upper()

    address = address_dict[db_name]
    channel = grpc.insecure_channel(address, options=options)
    stub = tenseal_data_pb2_grpc.DatabaseServerServiceStub(channel)
    return stub


def getKSStub(address_dict, options):
    address = address_dict["KEYSERVER"]
    channel = grpc.insecure_channel(address, options=options)
    stub = request_keyServer_pb2_grpc.KeyServerServiceStub(channel)

    return stub


"""
input: encrypted vector
return: decrypted vector
process: send request to KeyServer
"""


def resultsDecrypt(stub, enc_vector, proxy_request):
    serialize_msg = enc_vector.serialize()
    request = request_keyServer_pb2.requestEncResult(cid=proxy_request.cid, qid=proxy_request.qid,
                                                     ipaddress=proxy_request.ipaddress, encResult=serialize_msg)
    response = stub.RequestDecrypt(request)
    print(response)
