"""
parsing.py responses to parse the request from clients,
and return results
"""
from requestServer.utils import *


def requestParsing(request,pk_ctx):
    msg = request.op.upper()

    if msg == "MAX":
        enc_vector = getMaxValue(pk_ctx)
        return enc_vector

    if msg == "MIN":
        enc_vector = getMinValue(pk_ctx)
        return enc_vector

    if msg == "SUM":
        enc_vector = getSumValue(pk_ctx)
        return enc_vector

    if msg == "ADDMAX":
        enc_vector = getAddMaxValue(pk_ctx)
        return enc_vector

    if msg == "ADDSUM":
        enc_vector = getAddSumValue(pk_ctx)
        return enc_vector
