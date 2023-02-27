"""
parsing.py responses to parse the request from clients,
and return results
"""
import pickle

import hydra
from numpy import *
import tenseal as ts
from omegaconf import DictConfig

from .utils import *


# parse the request from client_proxy, divided into two schemes:local and total
def request_parsing(request, pk_ctx, address_dict, options):
    db_name = request.db_name.upper()

    if db_name == "TOTAL":
        enc_vector = process_total_request(request, pk_ctx, address_dict, options)
        return enc_vector

    else:
        db_stub = get_db_stub(request.db_name, address_dict, options)
        enc_vector = process_local_request(request, pk_ctx, db_stub)
        return enc_vector


# process the request in which query data_modeling is only from local database
def get_local_count(request, db_stub,n):
    mode = "encypted"
    if "CLEAN" in request.op:
        mode = "clean"
    n_th_query_msg = tenseal_data_server_pb2.n_th_query_msg(cid=request.cid, qid=request.qid, n = n,mode = mode, table_name=request.table_name,column_name=request.column_name)
    n_th_query_response = db_stub.n_th_query_operation(n_th_query_msg)
    return n_th_query_response

def process_local_request(request, pk_ctx, db_stub):
    query_request = tenseal_data_server_pb2.query_msg_parse_server(cid=request.cid, qid=request.qid, op=request.op,
                                                                   column_name=request.column_name,
                                                                   table_name=request.table_name)
    response = db_stub.query_operation(query_request)
    enc_vector = ts.ckks_vector_from(pk_ctx, response.enc_result)

    return enc_vector


# process the request in which query data_modeling is only from local database and needs noise.
def process_noise_local_request(request, db_stub):
    query_request = tenseal_data_server_pb2.query_msg_parse_server(cid=request.cid, qid=request.qid, op=request.op,
                                                                   column_name=request.column_name,
                                                                   table_name=request.table_name)
    response = db_stub.noise_query_operation(query_request)
    noise_vector = pickle.loads(response.enc_result)

    return noise_vector


# process the request which needs all dataServer participates
def get_n_th_list(request, db_stub_list, pk_ctx, n):
    n_th_list = []
    for stub in db_stub_list:
        n_th_query_response = get_local_count(request, stub, n)
        enc_vector = ts.ckks_vector_from(pk_ctx, n_th_query_response.result)
        hash_code = n_th_query_response.hash
        available = n_th_query_response.available
        if available:
            n_th_list.append((hash_code,enc_vector))
        else:
            n_th_list.append(None)
    return n_th_list

from typing import Tuple, Set
from typing import List

def is_n_th_enough(res_list: List[List[Tuple[int,object]]]):
    set_all: List[Set[int]] = []

    for res in range(len(res_list)):
        set_all.append(set())
        for item in res_list[res]:
            if item is not None:
                set_all[res].add(item[0])

    temp_and = set_all[0]
    temp_or = set_all[0]

    for set_ in set_all:
        temp_and = temp_and & set_
        temp_or = temp_or | set_

    return temp_and, temp_or


def get_encryped_total_frequency(hash_code, db_stub_list,pk_ctx):
    temp = None
    for stub in db_stub_list:
        query_request = tenseal_data_server_pb2.buffer_query_msg(hash=hash_code)
        response = stub.query_from_buffer(query_request)
        if response.available:
            enc_vector = ts.ckks_vector_from(pk_ctx, response.result)
            if temp is None:
                temp = enc_vector
            else:
                temp = temp + enc_vector

    return temp


def get_the_highest_hash(set_once: Set[int],key_stub,db_stub_list,pk_ctx):

    encryped_value: List[object] = []
    orderd_hash: List[int] = []
    for hash_code in set_once:
        orderd_hash.append(hash_code)
        encryped_value.append(get_encryped_total_frequency(hash_code,db_stub_list,pk_ctx))

    max_enc_vector = [encryped_value[0]]
    for enc_vector in encryped_value[1:]:
        sub_diff = max_enc_vector[0] - enc_vector
        nege_sub_diff = enc_vector - max_enc_vector[0]
        sub_serialize_msg = sub_diff.serialize()
        nege_sub_serialize_msg = nege_sub_diff.serialize()
        request = tenseal_key_server_pb2.vector(vector_msg=sub_serialize_msg)
        nege_request = tenseal_key_server_pb2.vector(vector_msg=nege_sub_serialize_msg)
        response = key_stub.boolean_positive(request)
        nege_response = key_stub.boolean_positive(nege_request)
        comparison_flag = response.bool_msg
        nege_comparison_flag = nege_response.bool_msg
        if not comparison_flag and nege_comparison_flag:
            max_enc_vector = enc_vector
        elif not comparison_flag and not nege_comparison_flag:
            max_enc_vector.append(enc_vector)

    list_hash = []

    for j in range(len(max_enc_vector)):
        for i in range(len(encryped_value)):
            if max_enc_vector[j] == encryped_value[i]:
                list_hash.append(orderd_hash[i])

    return list_hash

def get_enc_using_hash(hash_code,db_stub_list):
    for stub in db_stub_list:
        query_request = tenseal_data_server_pb2.query_mode_using_hash_msg(hash=hash_code)
        response = stub.query_mode_using_hash(query_request)
        if response.available:
            return response.mode

def get_total_var_mode(request, db_stub_list, pk_ctx, key_stub):
    from typing import Set
    set_all: Set[int] = set()
    set_once: Set[int] = set()
    res_list: List[List[Tuple[int,object]]] = []
    i = 0
    while len(set_all) != 1:
        if i == 0:
            request.op = "VAR_MODE_CLEAN"
        else:
            request.op = "VAR_MODE"
        i+= 1
        n_th_list = get_n_th_list(request, db_stub_list, pk_ctx, i-1)

        if n_th_list is None:
            # in case of the data is not enough
            highest_hash = get_the_highest_hash(set_once,key_stub,db_stub_list,pk_ctx)
            return ts.ckks_vector_from(pk_ctx,get_enc_using_hash(highest_hash,db_stub_list))

        res_list.append(n_th_list)

        set_all,set_once = is_n_th_enough(res_list)

    print(set_all,set_once)

    highest_hash_list = get_the_highest_hash(set_once,key_stub,db_stub_list,pk_ctx)

    encryped_vector_list = []

    for hash_code in highest_hash_list:
        encryped_vector_list.append(ts.ckks_vector_from(pk_ctx,get_enc_using_hash(hash_code,db_stub_list)))

    return encryped_vector_list

def get_total_var_median(request, db_stub_list, pk_ctx, key_stub):
    max = get_total_max(request, db_stub_list, pk_ctx, key_stub)
    min = get_total_min(request, db_stub_list, pk_ctx, key_stub)
    std_min = 0
    std_max = 1
    std_mid = (std_max+std_min)/2

    std = get_total_std(request, db_stub_list, pk_ctx, key_stub)
    avg = get_total_avg(request, db_stub_list, pk_ctx, key_stub)

    for i in range(10):
        std_min = (std_max+std_min)/2
        temp_mid = std_mid * max + (1 - std_mid) * min
        le_list = []
        g_list = []
        for stub in db_stub_list:
            query_request = tenseal_data_server_pb2.query_median_posi_msg(cid = request.cid, qid = request.qid, table_name = request.table_name, column_name = request.column_name, median = temp_mid.serialize(), std = std.serialize(), avg = avg.serialize())
            response = stub.query_median_posi(query_request)
            le = ts.ckks_vector_from(pk_ctx, response.less_e)
            g = ts.ckks_vector_from(pk_ctx, response.greater)
            le_list.append(le)
            g_list.append(g)

        le_sum = sum(le_list)
        g_sum = sum(g_list)

        sub_diff = le_sum - g_sum
        sub_serialize_msg = sub_diff.serialize()
        requests = tenseal_key_server_pb2.vector(vector_msg=sub_serialize_msg)
        response = key_stub.boolean_positive(requests)
        comparison_flag = response.bool_msg
        if comparison_flag:
            std_max = std_mid
        else:
            std_min = std_mid

    std_mid = (std_max + std_min) / 2
    return std_mid * max + (1 - std_mid) * min



def process_total_request(request, pk_ctx, address_dict, options):
    db_stub_list = get_all_db_stub(address_dict, options)
    op = request.op.upper()
    # sum value of column from all dataServer, op: count or sum

    # if op == "COUNT":
    #     key_stub = get_keyserver_stub(address_dict, options)
    #     count_vector = get_total_count(request, db_stub_list, key_stub)
    #     count_palin_vector = ts.plain_tensor(count_vector)
    #     count_enc_vector = ts.ckks_vector(pk_ctx, count_palin_vector)
    #     return count_enc_vector
    # max value of column from all dataServer
    if op == "MAX":
        key_stub = get_key_server_stub(address_dict, options)
        max_enc_vector = get_total_max(request, db_stub_list, pk_ctx, key_stub)
        return max_enc_vector
    # min value of column from all dataServer
    elif op == "MIN":
        key_stub = get_key_server_stub(address_dict, options)
        min_enc_vector = get_total_min(request, db_stub_list, pk_ctx, key_stub)
        return min_enc_vector
    # average value of column from all dataServer
    elif op == "AVG":
        key_stub = get_key_server_stub(address_dict, options)
        avg_enc_vector = get_total_avg(request, db_stub_list, pk_ctx, key_stub)
        return avg_enc_vector
    elif op == "VARIANCE":
        key_stub = get_key_server_stub(address_dict, options)
        # var_vector = get_total_var_dp(request, db_stub_list, key_stub)
        # var_palin_vector = ts.plain_tensor(var_vector)
        # var_enc_vector = ts.ckks_vector(pk_ctx, var_palin_vector)
        var_enc_vector = get_total_var(request, db_stub_list, pk_ctx, key_stub)
        return var_enc_vector
    elif op in ["STDDEV", "STD"]:
        key_stub = get_key_server_stub(address_dict, options)
        std_enc_vector = get_total_std(request, db_stub_list, pk_ctx, key_stub)
        return std_enc_vector
    elif op == "VAR_SAMP":
        key_stub = get_key_server_stub(address_dict, options)
        var_samp_enc_vector = get_total_var_samp(request, db_stub_list, pk_ctx, key_stub)
        return var_samp_enc_vector
    elif op == "STDDEV_SAMP":
        key_stub = get_key_server_stub(address_dict, options)
        std_samp_enc_vector = get_total_std_samp(request, db_stub_list, pk_ctx, key_stub)
        return std_samp_enc_vector
    elif op == "VAR_MODE":
        key_stub = get_key_server_stub(address_dict, options)
        var_mode_enc_vector = get_total_var_mode(request, db_stub_list, pk_ctx, key_stub)
        return var_mode_enc_vector
    elif op == "VAR_MEDIAN":
        key_stub = get_key_server_stub(address_dict, options)
        var_median_enc_vector = get_total_var_median(request, db_stub_list, pk_ctx, key_stub)
        return var_median_enc_vector
    else:
        sum_enc_vector = get_total_sum(request, db_stub_list, pk_ctx)
        return sum_enc_vector


# get all query result(encrypted vector) from data_server,stored in a list
def get_total_list(request, stub_list, pk_ctx):
    total_list = []
    for stub in stub_list:
        enc_vector = process_local_request(request, pk_ctx, stub)
        total_list.append(enc_vector)
    # sum_enc_vector = sum(total_list)
    return total_list


# get all query result with noise from data_server,stored in a list
def get_noise_total_list(request, db_stub_list):
    total_list = []
    for stub in db_stub_list:
        noise_vector = process_noise_local_request(request, stub)
        total_list.extend(noise_vector)
    return total_list


# sum all noise query results, get the plain sum
def get_noise_total_sum(request, db_stub_list):
    noise_total_list = get_noise_total_list(request, db_stub_list)
    print(noise_total_list)
    sum_noise_vector = sum(noise_total_list)
    return sum_noise_vector


# sum all query results, get the encrypted sum
def get_total_sum(request, db_stub_list, pk_ctx):
    total_list = get_total_list(request, db_stub_list, pk_ctx)
    sum_enc_vector = sum(total_list)
    return sum_enc_vector


# get the count over the total query result list with noise
def get_total_count_dp(request, db_stub_list, key_stub):
    sum_noise_vector = []
    generate_noise_request = tenseal_key_server_pb2.generate_noise_request(cid=request.cid, qid=request.qid,
                                                                           type="float")
    key_stub.generate_noise(generate_noise_request)
    noise_total_list = get_noise_total_list(request, db_stub_list)
    sum_noise = sum(noise_total_list)
    sum_noise_vector.append(sum_noise)

    return sum_noise_vector


# get the max encrypted vector over the total query result list
def get_total_max(request, db_stub_list, pk_ctx, key_stub): # TODO： 有可能出现两个一样的情况
    request.op = "max"
    total_list = get_total_list(request, db_stub_list, pk_ctx)

    max_enc_vector = total_list[0]
    for enc_vector in total_list[1:]:
        sub_diff = max_enc_vector - enc_vector
        sub_serialize_msg = sub_diff.serialize()
        request = tenseal_key_server_pb2.vector(vector_msg=sub_serialize_msg)
        response = key_stub.boolean_positive(request)
        comparison_flag = response.bool_msg
        if not comparison_flag:
            max_enc_vector = enc_vector
    return max_enc_vector


# get the min encrypted vector over the total query result list
def get_total_min(request, db_stub_list, pk_ctx, key_stub):
    request.op = "min"
    total_list = get_total_list(request, db_stub_list, pk_ctx)

    min_enc_vector = total_list[0]
    for enc_vector in total_list[1:]:
        sub_diff = min_enc_vector - enc_vector
        sub_serialize_msg = sub_diff.serialize()
        request = tenseal_key_server_pb2.vector(vector_msg=sub_serialize_msg)
        response = key_stub.boolean_positive(request)
        comparison_flag = response.bool_msg
        if comparison_flag:
            min_enc_vector = enc_vector
    return min_enc_vector


# get the average encrypted vector over the total query result list
def get_total_avg_dp(request, db_stub_list, pk_ctx, key_stub):
    # key_server generates noises foe the qid-th request
    generate_noise_request = tenseal_key_server_pb2.generate_noise_request(cid=request.cid, qid=request.qid,
                                                                           type="float")
    key_stub.generate_noise(generate_noise_request)
    # get the encrypted total sum
    request.op = "sum"
    total_list = get_total_list(request, db_stub_list, pk_ctx)
    sum_enc_vector = sum(total_list)

    # get the plain total count
    request.op = "count"
    # noise_count_sum = get_noise_total_sum(request, db_stub_list)
    # noise_count_sum = round(noise_count_sum)
    noise_count_sum = get_total_count_dp(request, db_stub_list, key_stub)
    noise_count_sum = round(noise_count_sum[0])

    avg_enc_vector = 1 / noise_count_sum * sum_enc_vector

    return avg_enc_vector


def get_total_avg(request, db_stub_list, pk_ctx, key_stub):
    # get the encrypted total sum
    request.op = "sum"
    total_enc_sum = get_total_sum(request, db_stub_list, pk_ctx)

    # get the encrypted total count
    request.op = "count"
    total_enc_count = get_total_sum(request, db_stub_list, pk_ctx)

    # get the average(sum/count) by calling the division interface provided by key_server
    total_enc_sum_msg = total_enc_sum.serialize()
    total_enc_count_msg = total_enc_count.serialize()
    div_request = tenseal_key_server_pb2.div_vectors(dividend_msg=total_enc_sum_msg, divisor_msg=total_enc_count_msg)
    div_response = key_stub.div_enc_vector(div_request)
    total_enc_avg_msg = div_response.vector_msg

    avg_enc_vector = ts.ckks_vector_from(pk_ctx, total_enc_avg_msg)
    return avg_enc_vector


# # get middle values for the total SD_Sample
def get_total_var_dp(request, db_stub_list, key_stub):
    generate_noise_request = tenseal_key_server_pb2.generate_noise_request(cid=request.cid, qid=request.qid,
                                                                           type="float")
    key_stub.generate_noise(generate_noise_request)
    request.op = "variance*count+avg*sum"
    noise_total_square_list = get_noise_total_list(request, db_stub_list)
    request.op = "sum"
    noise_total_sum_list = get_noise_total_list(request, db_stub_list)
    request.op = "count"
    noise_total_count_list = get_noise_total_list(request, db_stub_list)

    total_square = sum(noise_total_square_list)
    total_sum = sum(noise_total_sum_list)
    total_count = sum(noise_total_count_list)

    combined_var = [1 / total_count * (total_square - 1 / total_count * total_sum * total_sum)]

    return combined_var


# get the variance over the total query result list
# def get_total_var(request, db_stub_list, pk_ctx, key_stub):
#     # for each group,
#     request.op = "sum"
#     sum_total_list = get_total_list(request, db_stub_list, pk_ctx)
#     request.op = "count"
#     count_total_list = get_total_list(request, db_stub_list, pk_ctx)
#     total_count = get_total_count_dp(request, db_stub_list, key_stub)
#     total_count = round(total_count[0])
#     request.op = "variance"
#     var_total_list = get_total_list(request, db_stub_list, pk_ctx)
#     request.op = "avg"
#     avg_total_list = get_total_list(request, db_stub_list, pk_ctx)
#
#     square_x = multiply(var_total_list, count_total_list) + multiply(avg_total_list, sum_total_list)
#
#     total_sum = sum(sum_total_list)
#     total_square = sum(square_x)
#
#     combined_var = 1 / total_count * (total_square - 1 / total_count * total_sum * total_sum)
#
#     return combined_var

def get_mid_total_var(request, db_stub_list, pk_ctx, key_stub):
    # get the average,count,and variance*count+avg*sum(mid_result) over the total
    request.op = "avg"
    total_enc_avg = get_total_avg(request, db_stub_list, pk_ctx, key_stub)
    request.op = "count"
    total_enc_count = get_total_sum(request, db_stub_list, pk_ctx)
    request.op = "sum"
    total_enc_sum = get_total_sum(request, db_stub_list, pk_ctx)
    request.op = "variance*count+avg*sum"
    total_enc_mid_result = get_total_sum(request, db_stub_list, pk_ctx)

    return total_enc_sum, total_enc_avg, total_enc_count, total_enc_mid_result


def get_total_var(request, db_stub_list, pk_ctx, key_stub):
    total_enc_sum, total_enc_avg, total_enc_count, total_enc_mid_result = get_mid_total_var(request, db_stub_list,
                                                                                            pk_ctx, key_stub)
    # get the division result:total_mid_result/total_count
    total_enc_mid_result_msg = total_enc_mid_result.serialize()
    total_enc_count_msg = total_enc_count.serialize()
    div_request = tenseal_key_server_pb2.div_vectors(dividend_msg=total_enc_mid_result_msg,
                                                     divisor_msg=total_enc_count_msg)
    div_response = key_stub.div_enc_vector(div_request)
    div_enc_mid_msg = div_response.vector_msg
    div_enc_mid_vector = ts.ckks_vector_from(pk_ctx, div_enc_mid_msg)

    # combined_var = div_mid_enc_vector - avg*avg
    total_enc_var = div_enc_mid_vector - total_enc_avg * total_enc_avg

    return total_enc_var


def get_total_var_samp(request, db_stub_list, pk_ctx, key_stub):
    total_enc_sum, total_enc_avg, total_enc_count, total_enc_mid_result = get_mid_total_var(request, db_stub_list,
                                                                                            pk_ctx, key_stub)

    total_enc_mid_result_msg = total_enc_mid_result.serialize()
    divisor_vector_1 = total_enc_count - 1
    divisor_msg_1 = divisor_vector_1.serialize()
    div_request = tenseal_key_server_pb2.div_vectors(dividend_msg=total_enc_mid_result_msg,
                                                     divisor_msg=divisor_msg_1)
    div_response_1 = key_stub.div_enc_vector(div_request)
    div_enc_mid_msg_1 = div_response_1.vector_msg
    enc_mid_vector_1 = ts.ckks_vector_from(pk_ctx, div_enc_mid_msg_1)

    dividend_vector = total_enc_sum * total_enc_avg
    dividend_msg = dividend_vector.serialize()
    divisor_vector_2 = total_enc_count - 1
    divisor_msg = divisor_vector_2.serialize()
    div_request = tenseal_key_server_pb2.div_vectors(dividend_msg=dividend_msg, divisor_msg=divisor_msg)
    div_response_2 = key_stub.div_enc_vector(div_request)
    div_enc_mid_msg_2 = div_response_2.vector_msg
    enc_mid_vector_2 = ts.ckks_vector_from(pk_ctx, div_enc_mid_msg_2)

    total_enc_var_samp = enc_mid_vector_1 - enc_mid_vector_2

    return total_enc_var_samp


def get_total_std(request, db_stub_list, pk_ctx, key_stub):
    total_enc_var = get_total_var(request, db_stub_list, pk_ctx, key_stub)
    total_enc_var_msg = total_enc_var.serialize()
    sqrt_request = tenseal_key_server_pb2.vector(vector_msg=total_enc_var_msg)
    sqrt_response = key_stub.sqrt_enc_vector(sqrt_request)
    total_enc_std_msg = sqrt_response.vector_msg

    total_enc_std = ts.ckks_vector_from(pk_ctx, total_enc_std_msg)

    return total_enc_std


def get_total_std_samp(request, db_stub_list, pk_ctx, key_stub):
    total_enc_var_samp = get_total_var_samp(request, db_stub_list, pk_ctx, key_stub)

    total_enc_var_samp_msg = total_enc_var_samp.serialize()
    sqrt_request = tenseal_key_server_pb2.vector(vector_msg=total_enc_var_samp_msg)
    sqrt_response = key_stub.sqrt_enc_vector(sqrt_request)
    total_enc_std_samp_msg = sqrt_response.vector_msg

    total_enc_std_samp = ts.ckks_vector_from(pk_ctx, total_enc_std_samp_msg)

    return total_enc_std_samp
