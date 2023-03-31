# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tenseal_key_server.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x18tenseal_key_server.proto\x1a\x1bgoogle/protobuf/empty.proto\"]\n\x19query_result_parse_server\x12\x0b\n\x03\x63id\x18\x01 \x01(\x05\x12\x0b\n\x03qid\x18\x02 \x01(\x05\x12\x12\n\nip_address\x18\x03 \x01(\t\x12\x12\n\nenc_result\x18\x04 \x01(\x0c\"\x1c\n\x06vector\x12\x12\n\nvector_msg\x18\x01 \x01(\x0c\"8\n\x0b\x64iv_vectors\x12\x14\n\x0c\x64ividend_msg\x18\x01 \x01(\x0c\x12\x13\n\x0b\x64ivisor_msg\x18\x02 \x01(\x0c\"\"\n\x0e\x62oolean_result\x12\x10\n\x08\x62ool_msg\x18\x01 \x01(\x08\"@\n\x16generate_noise_request\x12\x0b\n\x03\x63id\x18\x01 \x01(\x05\x12\x0b\n\x03qid\x18\x02 \x01(\x05\x12\x0c\n\x04type\x18\x03 \x01(\t\">\n\x11get_noise_request\x12\x0f\n\x07\x64\x62_name\x18\x01 \x01(\x05\x12\x0b\n\x03\x63id\x18\x02 \x01(\x05\x12\x0b\n\x03qid\x18\x03 \x01(\x05\"\x1a\n\x05noise\x12\x11\n\tnoise_msg\x18\x01 \x01(\x0c\"\x16\n\x03raw\x12\x0f\n\x07raw_msg\x18\x01 \x01(\x01\x32\xb3\x05\n\x10KeyServerService\x12M\n\x17return_enc_query_result\x12\x1a.query_result_parse_server\x1a\x16.google.protobuf.Empty\x12\x41\n\x0egenerate_noise\x12\x17.generate_noise_request\x1a\x16.google.protobuf.Empty\x12\'\n\tget_noise\x12\x12.get_noise_request\x1a\x06.noise\x12,\n\x10\x62oolean_positive\x12\x07.vector\x1a\x0f.boolean_result\x12\x32\n\x16\x62oolean_positive_proxi\x12\x07.vector\x1a\x0f.boolean_result\x12/\n\x13\x62oolean_equal_proxi\x12\x07.vector\x1a\x0f.boolean_result\x12#\n\x0fsqrt_enc_vector\x12\x07.vector\x1a\x07.vector\x12\'\n\x0e\x64iv_enc_vector\x12\x0c.div_vectors\x1a\x07.vector\x12%\n\x11unpack_enc_vector\x12\x07.vector\x1a\x07.vector\x12\"\n\x06is_odd\x12\x07.vector\x1a\x0f.boolean_result\x12(\n\x0cis_sub_abs_1\x12\x07.vector\x1a\x0f.boolean_result\x12\x1b\n\x07sub_one\x12\x07.vector\x1a\x07.vector\x12\x36\n\x1a\x62oolean_positive_abs_proxi\x12\x07.vector\x1a\x0f.boolean_result\x12 \n\x0fshow_raw_vector\x12\x07.vector\x1a\x04.raw\x12\x17\n\x03\x61\x62s\x12\x07.vector\x1a\x07.vectorb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'tenseal_key_server_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _QUERY_RESULT_PARSE_SERVER._serialized_start=57
  _QUERY_RESULT_PARSE_SERVER._serialized_end=150
  _VECTOR._serialized_start=152
  _VECTOR._serialized_end=180
  _DIV_VECTORS._serialized_start=182
  _DIV_VECTORS._serialized_end=238
  _BOOLEAN_RESULT._serialized_start=240
  _BOOLEAN_RESULT._serialized_end=274
  _GENERATE_NOISE_REQUEST._serialized_start=276
  _GENERATE_NOISE_REQUEST._serialized_end=340
  _GET_NOISE_REQUEST._serialized_start=342
  _GET_NOISE_REQUEST._serialized_end=404
  _NOISE._serialized_start=406
  _NOISE._serialized_end=432
  _RAW._serialized_start=434
  _RAW._serialized_end=456
  _KEYSERVERSERVICE._serialized_start=459
  _KEYSERVERSERVICE._serialized_end=1150
# @@protoc_insertion_point(module_scope)
