# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
import transmission.tenseal.tenseal_client_proxy_pb2 as tenseal__client__proxy__pb2


class ClientProxyServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.data_query = channel.unary_unary(
                '/ClientProxyService/data_query',
                request_serializer=tenseal__client__proxy__pb2.query_msg_client.SerializeToString,
                response_deserializer=tenseal__client__proxy__pb2.dec_query_result.FromString,
                )
        self.return_dec_query_result = channel.unary_unary(
                '/ClientProxyService/return_dec_query_result',
                request_serializer=tenseal__client__proxy__pb2.query_result_key_server.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )


class ClientProxyServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def data_query(self, request, context):
        """clientProxy provides the interface, client remotes the call
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def return_dec_query_result(self, request, context):
        """clientProxy provides the interface, keyServer remotes the call
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ClientProxyServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'data_query': grpc.unary_unary_rpc_method_handler(
                    servicer.data_query,
                    request_deserializer=tenseal__client__proxy__pb2.query_msg_client.FromString,
                    response_serializer=tenseal__client__proxy__pb2.dec_query_result.SerializeToString,
            ),
            'return_dec_query_result': grpc.unary_unary_rpc_method_handler(
                    servicer.return_dec_query_result,
                    request_deserializer=tenseal__client__proxy__pb2.query_result_key_server.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'ClientProxyService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ClientProxyService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def data_query(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ClientProxyService/data_query',
            tenseal__client__proxy__pb2.query_msg_client.SerializeToString,
            tenseal__client__proxy__pb2.dec_query_result.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def return_dec_query_result(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ClientProxyService/return_dec_query_result',
            tenseal__client__proxy__pb2.query_result_key_server.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
