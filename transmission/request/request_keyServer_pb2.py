# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: request_keyServer.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x17request_keyServer.proto\x1a\x1bgoogle/protobuf/empty.proto\"R\n\x10requestEncResult\x12\x0b\n\x03\x63id\x18\x01 \x01(\x05\x12\x0b\n\x03qid\x18\x02 \x01(\x05\x12\x11\n\tipaddress\x18\x03 \x01(\t\x12\x11\n\tencResult\x18\x04 \x01(\x0c\"!\n\x0cvectorResult\x12\x11\n\tvectorMsg\x18\x01 \x01(\x0c\" \n\rbooleanResult\x12\x0f\n\x07\x62oolMsg\x18\x01 \x01(\x08\">\n\x14requestGenerateNoise\x12\x0b\n\x03\x63id\x18\x01 \x01(\x05\x12\x0b\n\x03qid\x18\x02 \x01(\x05\x12\x0c\n\x04type\x18\x03 \x01(\t\"<\n\x0frequestGetNoise\x12\x0f\n\x07\x64\x62_name\x18\x01 \x01(\x05\x12\x0b\n\x03\x63id\x18\x02 \x01(\x05\x12\x0b\n\x03qid\x18\x03 \x01(\x05\"!\n\rresponseNoise\x12\x10\n\x08noiseMsg\x18\x01 \x01(\x0c\x32\x9d\x02\n\x10KeyServerService\x12.\n\x0eRequestDecrypt\x12\r.vectorResult\x1a\r.vectorResult\x12\x39\n\x0cReturnResult\x12\x11.requestEncResult\x1a\x16.google.protobuf.Empty\x12\x30\n\x0f\x42ooleanPositive\x12\r.vectorResult\x1a\x0e.booleanResult\x12>\n\rGenerateNoise\x12\x15.requestGenerateNoise\x1a\x16.google.protobuf.Empty\x12,\n\x08GetNoise\x12\x10.requestGetNoise\x1a\x0e.responseNoiseb\x06proto3')



_REQUESTENCRESULT = DESCRIPTOR.message_types_by_name['requestEncResult']
_VECTORRESULT = DESCRIPTOR.message_types_by_name['vectorResult']
_BOOLEANRESULT = DESCRIPTOR.message_types_by_name['booleanResult']
_REQUESTGENERATENOISE = DESCRIPTOR.message_types_by_name['requestGenerateNoise']
_REQUESTGETNOISE = DESCRIPTOR.message_types_by_name['requestGetNoise']
_RESPONSENOISE = DESCRIPTOR.message_types_by_name['responseNoise']
requestEncResult = _reflection.GeneratedProtocolMessageType('requestEncResult', (_message.Message,), {
  'DESCRIPTOR' : _REQUESTENCRESULT,
  '__module__' : 'request_keyServer_pb2'
  # @@protoc_insertion_point(class_scope:requestEncResult)
  })
_sym_db.RegisterMessage(requestEncResult)

vectorResult = _reflection.GeneratedProtocolMessageType('vectorResult', (_message.Message,), {
  'DESCRIPTOR' : _VECTORRESULT,
  '__module__' : 'request_keyServer_pb2'
  # @@protoc_insertion_point(class_scope:vectorResult)
  })
_sym_db.RegisterMessage(vectorResult)

booleanResult = _reflection.GeneratedProtocolMessageType('booleanResult', (_message.Message,), {
  'DESCRIPTOR' : _BOOLEANRESULT,
  '__module__' : 'request_keyServer_pb2'
  # @@protoc_insertion_point(class_scope:booleanResult)
  })
_sym_db.RegisterMessage(booleanResult)

requestGenerateNoise = _reflection.GeneratedProtocolMessageType('requestGenerateNoise', (_message.Message,), {
  'DESCRIPTOR' : _REQUESTGENERATENOISE,
  '__module__' : 'request_keyServer_pb2'
  # @@protoc_insertion_point(class_scope:requestGenerateNoise)
  })
_sym_db.RegisterMessage(requestGenerateNoise)

requestGetNoise = _reflection.GeneratedProtocolMessageType('requestGetNoise', (_message.Message,), {
  'DESCRIPTOR' : _REQUESTGETNOISE,
  '__module__' : 'request_keyServer_pb2'
  # @@protoc_insertion_point(class_scope:requestGetNoise)
  })
_sym_db.RegisterMessage(requestGetNoise)

responseNoise = _reflection.GeneratedProtocolMessageType('responseNoise', (_message.Message,), {
  'DESCRIPTOR' : _RESPONSENOISE,
  '__module__' : 'request_keyServer_pb2'
  # @@protoc_insertion_point(class_scope:responseNoise)
  })
_sym_db.RegisterMessage(responseNoise)

_KEYSERVERSERVICE = DESCRIPTOR.services_by_name['KeyServerService']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _REQUESTENCRESULT._serialized_start=56
  _REQUESTENCRESULT._serialized_end=138
  _VECTORRESULT._serialized_start=140
  _VECTORRESULT._serialized_end=173
  _BOOLEANRESULT._serialized_start=175
  _BOOLEANRESULT._serialized_end=207
  _REQUESTGENERATENOISE._serialized_start=209
  _REQUESTGENERATENOISE._serialized_end=271
  _REQUESTGETNOISE._serialized_start=273
  _REQUESTGETNOISE._serialized_end=333
  _RESPONSENOISE._serialized_start=335
  _RESPONSENOISE._serialized_end=368
  _KEYSERVERSERVICE._serialized_start=371
  _KEYSERVERSERVICE._serialized_end=656
# @@protoc_insertion_point(module_scope)
