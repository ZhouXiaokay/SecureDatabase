import transmission.tenseal.tenseal_client_proxy_pb2 as tenseal_client_proxy_pb2
import transmission.tenseal.tenseal_client_proxy_pb2_grpc as tenseal_client_proxy_pb2_grpc
import transmission.tenseal.tenseal_parse_server_pb2 as tenseal_parse_server_pb2
import time
import pickle
from data_query.client_proxy.utils import *


class ClientProxy(tenseal_client_proxy_pb2_grpc.ClientProxyServiceServicer):
    def __init__(self, parse_server_address, address):
        self.parse_server_address = parse_server_address
        self.address = address
        self.max_msg_size = 1000000000
        self.options = [('grpc.max_send_message_length', self.max_msg_size),
                        ('grpc.max_receive_message_length', self.max_msg_size)]
        self.sleep_time = 0.1

        self.result_list = []

    def data_query(self, request, context):
        # get parse_server stub and send request query to parse_server
        parse_server_stub = get_parse_server_stub(self.parse_server_address, self.options)
        request_query = tenseal_parse_server_pb2.query_msg_client_proxy(cid=request.cid, qid=request.qid,
                                                                        db_name=request.db_name,
                                                                        column_name=request.column_name, op=request.op,
                                                                        table_name=request.table_name,
                                                                        ip_address=self.address)
        parse_server_stub.parse_request(request_query)

        while not boolean_find_result(request.cid, request.qid, self.result_list):
            time.sleep(self.sleep_time)
        result = get_result(request.cid, request.qid, self.result_list)
        if request.op.upper() == "COUNT":
            result = [round(x) for x in result]

        serialize_msg = pickle.dumps(result)

        response = tenseal_client_proxy_pb2.query_result(dec_result=serialize_msg)

        return response

    def return_dec_query_result(self, request, context):
        cid = request.cid
        qid = request.qid
        serialize_msg = request.dec_result
        result = pickle.loads(serialize_msg)
        result_dict = {'cid': cid, 'qid': qid, 'result': result}
        self.result_list.append(result_dict)

        response = tenseal_client_proxy_pb2.google_dot_protobuf_dot_empty__pb2.Empty()

        return response
