"""
parsing.py responses to parse the request from clients,
and return results
"""
from parseServer.utils import *
import pickle


# parse the request from clientProxy, divided into two schemes:local and total
def request_parsing(request, pk_ctx, address_dict, options):
    db_name = request.db_name.upper()

    if db_name == "TOTAL":
        enc_vector = process_total_request(request, pk_ctx, address_dict, options)
        return enc_vector

    else:
        db_stub = get_db_stub(request.db_name, address_dict, options)
        enc_vector = process_local_request(request, pk_ctx, db_stub)
        return enc_vector


# process the request in which query data is only from local database
def process_local_request(request, pk_ctx, db_stub):
    query_request = tenseal_data_pb2.requestOP(cid=request.cid, qid=request.qid, op=request.op,
                                               column_name=request.column_name,
                                               table_name=request.table_name)
    response = db_stub.QueryOperation(query_request)
    enc_vector = ts.ckks_vector_from(pk_ctx, response.encResult)

    return enc_vector


# process the request which need query result with noise
def process_noise_local_request(request, db_stub):
    query_request = tenseal_data_pb2.requestOP(cid=request.cid, qid=request.qid, op=request.op,
                                               column_name=request.column_name,
                                               table_name=request.table_name)
    response = db_stub.NoiseQueryOperation(query_request)
    noise_vector = pickle.loads(response.encResult)

    return noise_vector


# process the request which needs all dataServer participates
def process_total_request(request, pk_ctx, address_dict, options):
    db_stub_list = get_all_db_stub(address_dict, options)
    op = request.op.upper()
    # sum value of column from all dataServer, op: count or sum
    if op == "SUM" or op == "COUNT":
        sum_enc_vector = get_total_sum(request, db_stub_list, pk_ctx)
        return sum_enc_vector
    # max value of column from all dataServer
    elif op == "MAX":
        key_stub = get_keyserver_stub(address_dict, options)
        max_enc_vector = get_total_max(request, db_stub_list, pk_ctx, key_stub)
        return max_enc_vector
    # min value of column from all dataServer
    elif op == "MIN":
        key_stub = get_keyserver_stub(address_dict, options)
        min_enc_vector = get_total_min(request, db_stub_list, pk_ctx, key_stub)
        return min_enc_vector
    # average value of column from all dataServer
    elif op == "AVG":
        key_stub = get_keyserver_stub(address_dict, options)
        avg_enc_vector = get_total_avg(request, db_stub_list, pk_ctx, key_stub)
        return avg_enc_vector


# get all query result(encrypted vector) from databaseServer,stored in a list
def get_total_list(request, stub_list, pk_ctx):
    total_list = []
    for stub in stub_list:
        enc_vector = process_local_request(request, pk_ctx, stub)
        total_list.append(enc_vector)
    # sum_enc_vector = sum(total_list)
    return total_list


def get_noise_total_list(request, db_stub_list):
    total_list = []
    for stub in db_stub_list:
        noise_vector = process_noise_local_request(request, stub)
        total_list.extend(noise_vector)
    return total_list


def get_noise_total_sum(request, db_stub_list):
    noise_total_list = get_noise_total_list(request, db_stub_list)
    print(noise_total_list)
    sum_noise_vector = sum(noise_total_list)
    return sum_noise_vector


def get_total_sum(request, db_stub_list, pk_ctx):
    total_list = get_total_list(request, db_stub_list, pk_ctx)
    sum_enc_vector = sum(total_list)
    return sum_enc_vector


# get the max encrypted vector over the total query result list
def get_total_max(request, db_stub_list, pk_ctx, key_stub):
    request.op = "max"
    total_list = get_total_list(request, db_stub_list, pk_ctx)

    max_enc_vector = total_list[0]
    for enc_vector in total_list[1:]:
        sub_diff = max_enc_vector - enc_vector
        sub_serialize_msg = sub_diff.serialize()
        request = request_keyServer_pb2.vectorResult(vectorMsg=sub_serialize_msg)
        response = key_stub.BooleanPositive(request)
        comparison_flag = response.boolMsg
        if not comparison_flag:
            max_enc_vector = enc_vector
    return max_enc_vector


def get_total_min(request, db_stub_list, pk_ctx, key_stub):
    request.op = "min"
    total_list = get_total_list(request, db_stub_list, pk_ctx)

    min_enc_vector = total_list[0]
    for enc_vector in total_list[1:]:
        sub_diff = min_enc_vector - enc_vector
        sub_serialize_msg = sub_diff.serialize()
        request = request_keyServer_pb2.vectorResult(vectorMsg=sub_serialize_msg)
        response = key_stub.BooleanPositive(request)
        comparison_flag = response.boolMsg
        if comparison_flag:
            min_enc_vector = enc_vector
    return min_enc_vector


def get_total_avg(request, db_stub_list, pk_ctx, key_stub):
    generate_noise_request = request_keyServer_pb2.requestGenerateNoise(cid=request.cid, qid=request.qid,
                                                                        type="float")
    key_stub.GenerateNoise(generate_noise_request)
    request.op = "sum"
    total_list = get_total_list(request, db_stub_list, pk_ctx)
    sum_enc_vector = sum(total_list)

    request.op = "count"
    noise_count_sum = get_noise_total_sum(request, db_stub_list)
    noise_count_sum = round(noise_count_sum)

    avg_enc_vector = 1 / noise_count_sum * sum_enc_vector

    return avg_enc_vector
