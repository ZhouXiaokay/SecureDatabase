import transmission.teanseal.tenseal_data_pb2_grpc as tenseal_data_pb2_grpc
import transmission.teanseal.tenseal_data_pb2 as tenseal_data_pb2
import tenseal as ts
from databaseServer.conn_mysql import *


class DatabaseServer(tenseal_data_pb2_grpc.SafeTransmissionServicer):

    def __init__(self, address, pk_ctx_file, name):
        self.address = address
        pk_bytes = open(pk_ctx_file, "rb").read()
        self.pk_ctx = ts.context_from(pk_bytes)
        self.sleep_time = 0.01
        self.name = name

    def MaxValue(self, request, context):
        maxvalue = getMaxValue(self.name)

        plain_vector = ts.plain_tensor([maxvalue])
        enc_vector = ts.ckks_vector(self.pk_ctx, plain_vector)
        serialize_msg = enc_vector.serialize()
        response = tenseal_data_pb2.encrypted(id=1, msg=serialize_msg)

        return response

    def MinValue(self, request, context):
        minvalue = getMinValue(self.name)

        plain_vector = ts.plain_tensor([minvalue])
        enc_vector = ts.ckks_vector(self.pk_ctx, plain_vector)
        serialize_msg = enc_vector.serialize()
        response = tenseal_data_pb2.encrypted(id=1, msg=serialize_msg)

        return response

    def SumValue(self, request, context):
        sumValue = getSumValue(self.name)

        plain_vector = ts.plain_tensor([sumValue])
        enc_vector = ts.ckks_vector(self.pk_ctx, plain_vector)
        serialize_msg = enc_vector.serialize()
        response = tenseal_data_pb2.encrypted(id=1, msg=serialize_msg)

        return response


