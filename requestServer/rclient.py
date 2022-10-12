import transmission.teanseal.tenseal_data_pb2_grpc as tenseal_data_pb2_grpc
import transmission.teanseal.tenseal_data_pb2 as tenseal_data_pb2
import tenseal as ts
import grpc
def run(pk_ctx):
    max_msg_size = 1000000000
    options = [('grpc.max_send_message_length', max_msg_size),
               ('grpc.max_receive_message_length', max_msg_size)]
    channel = grpc.insecure_channel('127.0.0.1:50051', options=options)
    stub = tenseal_data_pb2_grpc.SafeTransmissionStub(channel)

    request = tenseal_data_pb2.requestOP(id="",op="")
    response = stub.MaxValue(request)
    enc_vector_1 = ts.ckks_vector_from(pk_ctx,response.msg)

    return enc_vector_1



if __name__ == "__main__":

    pk_file = "../transmission/ts_ckks_pk.config"
    pk_bytes = open(pk_file,"rb").read()
    pk_ctx = ts.context_from(pk_bytes)

    enc1 = run(pk_ctx)



    sk_ctx_file = "../transmission/ts_ckks.config"
    sk_context_bytes = open(sk_ctx_file,"rb").read()
    ctx = ts.context_from(sk_context_bytes)
    sk = ctx.secret_key()

    print(enc1.decrypt(sk))
    print(enc1.decrypt())


