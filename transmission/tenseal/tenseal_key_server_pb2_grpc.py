# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
import transmission.tenseal.tenseal_key_server_pb2 as tenseal__key__server__pb2


class KeyServerServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.return_enc_query_result = channel.unary_unary(
                '/KeyServerService/return_enc_query_result',
                request_serializer=tenseal__key__server__pb2.query_result_parse_server.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.generate_noise = channel.unary_unary(
                '/KeyServerService/generate_noise',
                request_serializer=tenseal__key__server__pb2.generate_noise_request.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.get_noise = channel.unary_unary(
                '/KeyServerService/get_noise',
                request_serializer=tenseal__key__server__pb2.get_noise_request.SerializeToString,
                response_deserializer=tenseal__key__server__pb2.noise.FromString,
                )
        self.boolean_positive = channel.unary_unary(
                '/KeyServerService/boolean_positive',
                request_serializer=tenseal__key__server__pb2.vector.SerializeToString,
                response_deserializer=tenseal__key__server__pb2.boolean_result.FromString,
                )
        self.sqrt_enc_vector = channel.unary_unary(
                '/KeyServerService/sqrt_enc_vector',
                request_serializer=tenseal__key__server__pb2.vector.SerializeToString,
                response_deserializer=tenseal__key__server__pb2.vector.FromString,
                )
        self.div_enc_vector = channel.unary_unary(
                '/KeyServerService/div_enc_vector',
                request_serializer=tenseal__key__server__pb2.div_vectors.SerializeToString,
                response_deserializer=tenseal__key__server__pb2.vector.FromString,
                )


class KeyServerServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def return_enc_query_result(self, request, context):
        """requestServer remotes the call and keyServer send decrypted result to clientProxy
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def generate_noise(self, request, context):
        """requestServer remotes the call, and keyServer generates noise list
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get_noise(self, request, context):
        """dataServer remotes the call, and keyServer sends noise back
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def boolean_positive(self, request, context):
        """keyServer provides the following operations: division,sqrt,boolean positive
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def sqrt_enc_vector(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def div_enc_vector(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_KeyServerServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'return_enc_query_result': grpc.unary_unary_rpc_method_handler(
                    servicer.return_enc_query_result,
                    request_deserializer=tenseal__key__server__pb2.query_result_parse_server.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'generate_noise': grpc.unary_unary_rpc_method_handler(
                    servicer.generate_noise,
                    request_deserializer=tenseal__key__server__pb2.generate_noise_request.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'get_noise': grpc.unary_unary_rpc_method_handler(
                    servicer.get_noise,
                    request_deserializer=tenseal__key__server__pb2.get_noise_request.FromString,
                    response_serializer=tenseal__key__server__pb2.noise.SerializeToString,
            ),
            'boolean_positive': grpc.unary_unary_rpc_method_handler(
                    servicer.boolean_positive,
                    request_deserializer=tenseal__key__server__pb2.vector.FromString,
                    response_serializer=tenseal__key__server__pb2.boolean_result.SerializeToString,
            ),
            'sqrt_enc_vector': grpc.unary_unary_rpc_method_handler(
                    servicer.sqrt_enc_vector,
                    request_deserializer=tenseal__key__server__pb2.vector.FromString,
                    response_serializer=tenseal__key__server__pb2.vector.SerializeToString,
            ),
            'div_enc_vector': grpc.unary_unary_rpc_method_handler(
                    servicer.div_enc_vector,
                    request_deserializer=tenseal__key__server__pb2.div_vectors.FromString,
                    response_serializer=tenseal__key__server__pb2.vector.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'KeyServerService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class KeyServerService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def return_enc_query_result(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/KeyServerService/return_enc_query_result',
            tenseal__key__server__pb2.query_result_parse_server.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def generate_noise(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/KeyServerService/generate_noise',
            tenseal__key__server__pb2.generate_noise_request.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def get_noise(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/KeyServerService/get_noise',
            tenseal__key__server__pb2.get_noise_request.SerializeToString,
            tenseal__key__server__pb2.noise.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def boolean_positive(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/KeyServerService/boolean_positive',
            tenseal__key__server__pb2.vector.SerializeToString,
            tenseal__key__server__pb2.boolean_result.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def sqrt_enc_vector(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/KeyServerService/sqrt_enc_vector',
            tenseal__key__server__pb2.vector.SerializeToString,
            tenseal__key__server__pb2.vector.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def div_enc_vector(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/KeyServerService/div_enc_vector',
            tenseal__key__server__pb2.div_vectors.SerializeToString,
            tenseal__key__server__pb2.vector.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)