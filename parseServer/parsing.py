"""
parsing.py responses to parse the request from clients,
and return results
"""
from parseServer.utils import *


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


# process the request which query data from local database
def process_local_request(request, pk_ctx, db_stub):
    query_request = tenseal_data_pb2.requestOP(op=request.op, column_name=request.column_name,
                                               table_name=request.table_name)
    response = db_stub.QueryOperation(query_request)
    enc_vector = ts.ckks_vector_from(pk_ctx, response.encResult)

    return enc_vector


# process the request which needs all dataServer participates
def process_total_request(request, pk_ctx, address_dict, options):
    db_stub_list = get_all_db_stub(address_dict, options)
    op = request.op.upper()
    # sum value of column
    if op == "SUM" or op == "COUNT":
        sum_enc_vector = get_total_sum(request, db_stub_list, pk_ctx)
        return sum_enc_vector
    # the number of column
    # average value of column
    if op == "AVG":
        avg_enc_vector = get_total_avg(request, db_stub_list, pk_ctx, address_dict, options)

        return avg_enc_vector


def process_noise_local_request(request, db_stub):
    query_request = tenseal_data_pb2.requestOP(op=request.op, column_name=request.column_name,
                                               table_name=request.table_name)
    response = db_stub.NoiseQueryOperation(query_request)
    noise_vector = pickle.loads(response.encResult)

    return noise_vector


# get sum from all databaseServer
def get_total_sum(request, stub_list, pk_ctx):
    sum_list = []
    for stub in stub_list:
        enc_vector = process_local_request(request, pk_ctx, stub)
        sum_list.append(enc_vector)
    sum_enc_vector = sum(sum_list)
    return sum_enc_vector


def get_noise_total_sum(request, stub_list):
    sum_list = []
    for stub in stub_list:
        noise_vector = process_noise_local_request(request, stub)
        sum_list.extend(noise_vector)
    sum_noise_vector = sum(sum_list)
    return sum_noise_vector


# get count from all databaseServer
# def get_total_avg(request, db_stub_list, pk_ctx, address_dict, options):
#     request.op = "sum"
#     sum_enc_vector = get_total_sum(request, db_stub_list, pk_ctx)
#     request.op = "count"
#     count_enc_vector = get_total_sum(request, db_stub_list, pk_ctx)
#
#     key_stub = get_keyserver_stub(address_dict, options)
#     count_dec_vector = decrypt_results(key_stub, count_enc_vector)
#     print(count_dec_vector)
#     avg_enc_vector = 1 / count_dec_vector[0] * sum_enc_vector
#
#     return avg_enc_vector
def get_total_avg(request, db_stub_list, pk_ctx, address_dict, options):
    request.op = "sum"
    sum_enc_vector = get_total_sum(request, db_stub_list, pk_ctx)
    request.op = "count"
    noise_count_sum = get_noise_total_sum(request, db_stub_list)
    noise_count_sum = round(noise_count_sum)

    avg_enc_vector = 1 / noise_count_sum * sum_enc_vector

    return avg_enc_vector
