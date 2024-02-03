# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
import transmission.request.request_data_pb2 as request__data__pb2


class RequestTransmissionStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.RequestProxy = channel.unary_unary(
                '/RequestTransmission/RequestProxy',
                request_serializer=request__data__pb2.requestProxy.SerializeToString,
                response_deserializer=request__data__pb2.responseResult.FromString,
                )
        self.RequestParsing = channel.unary_unary(
                '/RequestTransmission/RequestParsing',
                request_serializer=request__data__pb2.requestQuery.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.RequestDecrypt = channel.unary_unary(
                '/RequestTransmission/RequestDecrypt',
                request_serializer=request__data__pb2.requestEncResult.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.RequestResult = channel.unary_unary(
                '/RequestTransmission/RequestResult',
                request_serializer=request__data__pb2.requestDecResult.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )


class RequestTransmissionServicer(object):
    """Missing associated documentation comment in .proto file."""

    def RequestProxy(self, request, context):
        """clientProxy provides the interface, client remotes the call
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RequestParsing(self, request, context):
        """parseServer provides the interface, clientProxy remotes the call
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RequestDecrypt(self, request, context):
        """keyServer provides the interface, parseServer remotes the call
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


def add_RequestTransmissionServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'RequestProxy': grpc.unary_unary_rpc_method_handler(
                    servicer.RequestProxy,
                    request_deserializer=request__data__pb2.requestProxy.FromString,
                    response_serializer=request__data__pb2.responseResult.SerializeToString,
            ),
            'RequestParsing': grpc.unary_unary_rpc_method_handler(
                    servicer.RequestParsing,
                    request_deserializer=request__data__pb2.requestQuery.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'RequestDecrypt': grpc.unary_unary_rpc_method_handler(
                    servicer.RequestDecrypt,
                    request_deserializer=request__data__pb2.requestEncResult.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'RequestResult': grpc.unary_unary_rpc_method_handler(
                    servicer.RequestResult,
                    request_deserializer=request__data__pb2.requestDecResult.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'RequestTransmission', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class RequestTransmission(object):
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
        return grpc.experimental.unary_unary(request, target, '/RequestTransmission/RequestProxy',
            request__data__pb2.requestProxy.SerializeToString,
            request__data__pb2.responseResult.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RequestParsing(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/RequestTransmission/RequestParsing',
            request__data__pb2.requestQuery.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RequestDecrypt(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/RequestTransmission/RequestDecrypt',
            request__data__pb2.requestEncResult.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/RequestTransmission/RequestResult',
            request__data__pb2.requestDecResult.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)