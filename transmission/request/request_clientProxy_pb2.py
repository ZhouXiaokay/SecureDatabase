# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: request_clientProxy.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x19request_clientProxy.proto\x1a\x1bgoogle/protobuf/empty.proto\"n\n\x0crequestProxy\x12\x0b\n\x03\x63id\x18\x01 \x01(\x05\x12\x0b\n\x03qid\x18\x02 \x01(\x05\x12\x0f\n\x07\x64\x62_name\x18\x03 \x01(\t\x12\x12\n\ntable_name\x18\x04 \x01(\t\x12\x13\n\x0b\x63olumn_name\x18\x05 \x01(\t\x12\n\n\x02op\x18\x06 \x01(\t\"?\n\x10requestDecResult\x12\x0b\n\x03\x63id\x18\x01 \x01(\x05\x12\x0b\n\x03qid\x18\x02 \x01(\x05\x12\x11\n\tdecResult\x18\x03 \x01(\x0c\" \n\x0eresponseResult\x12\x0e\n\x06result\x18\x01 \x01(\x0c\"\x14\n\x04\x66lag\x12\x0c\n\x04\x66lag\x18\x01 \x01(\x08\x32\x80\x01\n\x12\x43lientProxyService\x12.\n\x0cRequestProxy\x12\r.requestProxy\x1a\x0f.responseResult\x12:\n\rRequestResult\x12\x11.requestDecResult\x1a\x16.google.protobuf.Emptyb\x06proto3')



_REQUESTPROXY = DESCRIPTOR.message_types_by_name['requestProxy']
_REQUESTDECRESULT = DESCRIPTOR.message_types_by_name['requestDecResult']
_RESPONSERESULT = DESCRIPTOR.message_types_by_name['responseResult']
_FLAG = DESCRIPTOR.message_types_by_name['flag']
requestProxy = _reflection.GeneratedProtocolMessageType('requestProxy', (_message.Message,), {
  'DESCRIPTOR' : _REQUESTPROXY,
  '__module__' : 'request_clientProxy_pb2'
  # @@protoc_insertion_point(class_scope:requestProxy)
  })
_sym_db.RegisterMessage(requestProxy)

requestDecResult = _reflection.GeneratedProtocolMessageType('requestDecResult', (_message.Message,), {
  'DESCRIPTOR' : _REQUESTDECRESULT,
  '__module__' : 'request_clientProxy_pb2'
  # @@protoc_insertion_point(class_scope:requestDecResult)
  })
_sym_db.RegisterMessage(requestDecResult)

responseResult = _reflection.GeneratedProtocolMessageType('responseResult', (_message.Message,), {
  'DESCRIPTOR' : _RESPONSERESULT,
  '__module__' : 'request_clientProxy_pb2'
  # @@protoc_insertion_point(class_scope:responseResult)
  })
_sym_db.RegisterMessage(responseResult)

flag = _reflection.GeneratedProtocolMessageType('flag', (_message.Message,), {
  'DESCRIPTOR' : _FLAG,
  '__module__' : 'request_clientProxy_pb2'
  # @@protoc_insertion_point(class_scope:flag)
  })
_sym_db.RegisterMessage(flag)

_CLIENTPROXYSERVICE = DESCRIPTOR.services_by_name['ClientProxyService']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _REQUESTPROXY._serialized_start=58
  _REQUESTPROXY._serialized_end=168
  _REQUESTDECRESULT._serialized_start=170
  _REQUESTDECRESULT._serialized_end=233
  _RESPONSERESULT._serialized_start=235
  _RESPONSERESULT._serialized_end=267
  _FLAG._serialized_start=269
  _FLAG._serialized_end=289
  _CLIENTPROXYSERVICE._serialized_start=292
  _CLIENTPROXYSERVICE._serialized_end=420
# @@protoc_insertion_point(module_scope)