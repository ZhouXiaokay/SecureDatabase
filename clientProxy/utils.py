import transmission.request.request_parseServer_pb2_grpc as request_parseServer_pb2_grpc
import transmission.request.request_parseServer_pb2 as request_parseServer_pb2
import grpc


def getPSStub(requestServer_address, options):
    channel = grpc.insecure_channel(requestServer_address, options=options)
    stub = request_parseServer_pb2_grpc.ParseServerServiceStub(channel)
    return stub


def findResult(cid, qid, resultList):
    flag = False
    for result in resultList:
        if result['cid'] == cid and result['qid'] == qid:
            flag = True
            return flag
    return flag


def getResult(cid, qid, resultList):
    for result in resultList:
        if result['cid'] == cid and result['qid'] == qid:
            t = result['result']
            resultList.remove(result)
            return t
