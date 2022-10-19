import transmission.request.request_keyServer_pb2 as request_keyServer_pb2
import transmission.request.request_keyServer_pb2_grpc as request_keyServer_pb2_grpc
import transmission.request.request_clientProxy_pb2 as request_clientProxy_pb2
import transmission.request.request_clientProxy_pb2_grpc as request_clientProxy_pb2_grpc
import grpc
import tenseal as ts
import pickle
from clientProxy import ClientProxy


class KeyServer(request_keyServer_pb2_grpc.KeyServerServiceServicer):

    def __init__(self, sk_ctx_file):
        sk_ctx_bytes = open(sk_ctx_file, "rb").read()
        self.sk_ctx = ts.context_from(sk_ctx_bytes)
        self.max_msg_size = 1000000000
        self.options = [('grpc.max_send_message_length', self.max_msg_size),
                        ('grpc.max_receive_message_length', self.max_msg_size)]

    def RequestDecrypt(self, request, context):
        # receive and decrypt the results from parseServer
        ipaddress = request.ipaddress
        enc_serialize_msg = request.encResult
        enc_vector = ts.ckks_vector_from(self.sk_ctx, enc_serialize_msg)
        dec_vector = enc_vector.decrypt()
        print(dec_vector)

        # make request and send it to clientProxy
        dec_serialize_msg = pickle.dumps(dec_vector)
        result_request = request_clientProxy_pb2.requestDecResult(cid=request.cid, qid=request.qid,
                                                                  decResult=dec_serialize_msg)

        channel = grpc.insecure_channel(ipaddress, options=self.options)
        stub = request_clientProxy_pb2_grpc.ClientProxyServiceStub(channel)
        stub.RequestResult(result_request)

        response = request_keyServer_pb2.google_dot_protobuf_dot_empty__pb2.Empty()

        return response
