# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
import transmission.request.request_clientProxy_pb2 as request__clientProxy__pb2


class ClientProxyServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.RequestProxy = channel.unary_unary(
                '/ClientProxyService/RequestProxy',
                request_serializer=request__clientProxy__pb2.requestProxy.SerializeToString,
                response_deserializer=request__clientProxy__pb2.responseResult.FromString,
                )
        self.RequestResult = channel.unary_unary(
                '/ClientProxyService/RequestResult',
                request_serializer=request__clientProxy__pb2.requestDecResult.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )


class ClientProxyServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def RequestProxy(self, request, context):
        """clientProxy provides the interface, client remotes the call
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RequestResult(self, request, context):
        """clientProxy provides the interface, keyServer remotes the call
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ClientProxyServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'RequestProxy': grpc.unary_unary_rpc_method_handler(
                    servicer.RequestProxy,
                    request_deserializer=request__clientProxy__pb2.requestProxy.FromString,
                    response_serializer=request__clientProxy__pb2.responseResult.SerializeToString,
            ),
            'RequestResult': grpc.unary_unary_rpc_method_handler(
                    servicer.RequestResult,
                    request_deserializer=request__clientProxy__pb2.requestDecResult.FromString,
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
    def RequestProxy(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ClientProxyService/RequestProxy',
            request__clientProxy__pb2.requestProxy.SerializeToString,
            request__clientProxy__pb2.responseResult.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RequestResult(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ClientProxyService/RequestResult',
            request__clientProxy__pb2.requestDecResult.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
