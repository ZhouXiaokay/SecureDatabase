import transmission.request.request_clientProxy_pb2 as request_clientProxy_pb2
import transmission.request.request_clientProxy_pb2_grpc as request_clientProxy_pb2_grpc
import time
import grpc
import pickle
from clientProxy.utils import *


class ClientProxy(request_clientProxy_pb2_grpc.ClientProxyServiceServicer):
    def __init__(self, requestServer_address, address):
        self.requestServer_address = requestServer_address
        self.address = address
        self.max_msg_size = 1000000000
        self.options = [('grpc.max_send_message_length', self.max_msg_size),
                        ('grpc.max_receive_message_length', self.max_msg_size)]
        self.sleep_time = 0.1

        self.result_list = []

    def RequestProxy(self, request, context):
        # get parseServer stub and send request query to parseServer
        ps_stub = get_parse_server_stub(self.requestServer_address, self.options)
        request_query = request_parseServer_pb2.requestQuery(cid=request.cid, qid=request.qid, db_name=request.db_name,
                                                             column_name=request.column_name, op=request.op,
                                                             table_name=request.table_name,
                                                             ipaddress=self.address)
        ps_stub.RequestParsing(request_query)

        while not boolean_find_result(request.cid, request.qid, self.result_list):
            time.sleep(self.sleep_time)
        result = get_result(request.cid, request.qid, self.result_list)
        if request.op.upper() == "COUNT":
            result = [round(x) for x in result]

        serialize_msg = pickle.dumps(result)

        response = request_clientProxy_pb2.responseResult(result=serialize_msg)

        return response

    def RequestResult(self, request, context):
        cid = request.cid
        qid = request.qid
        serialize_msg = request.decResult
        result = pickle.loads(serialize_msg)
        result_dict = {'cid': cid, 'qid': qid, 'result': result}
        self.result_list.append(result_dict)

        response = request_clientProxy_pb2.google_dot_protobuf_dot_empty__pb2.Empty()

        return response
