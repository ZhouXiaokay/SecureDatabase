# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tenseal_client_proxy.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1atenseal_client_proxy.proto\x1a\x1bgoogle/protobuf/empty.proto\"r\n\x10query_msg_client\x12\x0b\n\x03\x63id\x18\x01 \x01(\x05\x12\x0b\n\x03qid\x18\x02 \x01(\x05\x12\x0f\n\x07\x64\x62_name\x18\x03 \x01(\t\x12\x12\n\ntable_name\x18\x04 \x01(\t\x12\x13\n\x0b\x63olumn_name\x18\x05 \x01(\t\x12\n\n\x02op\x18\x06 \x01(\t\"\"\n\x0cquery_result\x12\x12\n\ndec_result\x18\x01 \x01(\x0c\"G\n\x17query_result_key_server\x12\x0b\n\x03\x63id\x18\x01 \x01(\x05\x12\x0b\n\x03qid\x18\x02 \x01(\x05\x12\x12\n\ndec_result\x18\x03 \x01(\x0c\x32\x91\x01\n\x12\x43lientProxyService\x12.\n\ndata_query\x12\x11.query_msg_client\x1a\r.query_result\x12K\n\x17return_dec_query_result\x12\x18.query_result_key_server\x1a\x16.google.protobuf.Emptyb\x06proto3')



_QUERY_MSG_CLIENT = DESCRIPTOR.message_types_by_name['query_msg_client']
_QUERY_RESULT = DESCRIPTOR.message_types_by_name['query_result']
_QUERY_RESULT_KEY_SERVER = DESCRIPTOR.message_types_by_name['query_result_key_server']
query_msg_client = _reflection.GeneratedProtocolMessageType('query_msg_client', (_message.Message,), {
  'DESCRIPTOR' : _QUERY_MSG_CLIENT,
  '__module__' : 'tenseal_client_proxy_pb2'
  # @@protoc_insertion_point(class_scope:query_msg_client)
  })
_sym_db.RegisterMessage(query_msg_client)

query_result = _reflection.GeneratedProtocolMessageType('query_result', (_message.Message,), {
  'DESCRIPTOR' : _QUERY_RESULT,
  '__module__' : 'tenseal_client_proxy_pb2'
  # @@protoc_insertion_point(class_scope:query_result)
  })
_sym_db.RegisterMessage(query_result)

query_result_key_server = _reflection.GeneratedProtocolMessageType('query_result_key_server', (_message.Message,), {
  'DESCRIPTOR' : _QUERY_RESULT_KEY_SERVER,
  '__module__' : 'tenseal_client_proxy_pb2'
  # @@protoc_insertion_point(class_scope:query_result_key_server)
  })
_sym_db.RegisterMessage(query_result_key_server)

_CLIENTPROXYSERVICE = DESCRIPTOR.services_by_name['ClientProxyService']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _QUERY_MSG_CLIENT._serialized_start=59
  _QUERY_MSG_CLIENT._serialized_end=173
  _QUERY_RESULT._serialized_start=175
  _QUERY_RESULT._serialized_end=209
  _QUERY_RESULT_KEY_SERVER._serialized_start=211
  _QUERY_RESULT_KEY_SERVER._serialized_end=282
  _CLIENTPROXYSERVICE._serialized_start=285
  _CLIENTPROXYSERVICE._serialized_end=430
# @@protoc_insertion_point(module_scope)
