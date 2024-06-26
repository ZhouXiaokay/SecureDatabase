import transmission.request.request_parseServer_pb2_grpc as request_parseServer_pb2_grpc
import transmission.request.request_parseServer_pb2 as request_parseServer_pb2
import grpc


def get_parse_server_stub(parse_server_address, options):
    channel = grpc.insecure_channel(parse_server_address, options=options)
    stub = request_parseServer_pb2_grpc.ParseServerServiceStub(channel)
    return stub


def boolean_find_result(cid, qid, result_list):
    flag = False
    for result in result_list:
        if result['cid'] == cid and result['qid'] == qid:
            flag = True
            return flag
    return flag


def get_result(cid, qid, result_list):
    for result in result_list:
        if result['cid'] == cid and result['qid'] == qid:
            t = result['result']
            result_list.remove(result)
            return t
