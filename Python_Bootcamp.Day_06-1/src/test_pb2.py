# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: test.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\ntest.proto\"\x19\n\x07Request\x12\x0e\n\x06\x63oords\x18\x01 \x03(\x02\"\x1d\n\x05Reply\x12\x14\n\x05ships\x18\x01 \x03(\x0b\x32\x05.Ship\"\xa5\x03\n\x04Ship\x12\"\n\talignment\x18\x01 \x01(\x0e\x32\x0f.Ship.Alignment\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x1f\n\nship_class\x18\x03 \x01(\x0e\x32\x0b.Ship.Class\x12\x0e\n\x06length\x18\x04 \x01(\x02\x12\x11\n\tcrew_size\x18\x05 \x01(\x05\x12\r\n\x05\x61rmed\x18\x06 \x01(\x08\x12\x1f\n\x08officers\x18\x07 \x03(\x0b\x32\r.Ship.Officer\x1a>\n\x07Officer\x12\x12\n\nfirst_name\x18\x01 \x01(\t\x12\x11\n\tlast_name\x18\x02 \x01(\t\x12\x0c\n\x04rank\x18\x03 \x01(\t\"4\n\tAlignment\x12\x12\n\x0e\x41LIGNMENT_ALLY\x10\x01\x12\x13\n\x0f\x41LIGNMENT_ENEMY\x10\x02\"\x80\x01\n\x05\x43lass\x12\x12\n\x0e\x43LASS_CORVETTE\x10\x01\x12\x11\n\rCLASS_FRIGATE\x10\x02\x12\x11\n\rCLASS_CRUISER\x10\x03\x12\x13\n\x0f\x43LASS_DESTROYER\x10\x04\x12\x11\n\rCLASS_CARRIER\x10\x05\x12\x15\n\x11\x43LASS_DREADNOUGHT\x10\x06\x32)\n\x07Service\x12\x1e\n\x08SendData\x12\x08.Request\x1a\x06.Reply\"\x00')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'test_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_REQUEST']._serialized_start=14
  _globals['_REQUEST']._serialized_end=39
  _globals['_REPLY']._serialized_start=41
  _globals['_REPLY']._serialized_end=70
  _globals['_SHIP']._serialized_start=73
  _globals['_SHIP']._serialized_end=494
  _globals['_SHIP_OFFICER']._serialized_start=247
  _globals['_SHIP_OFFICER']._serialized_end=309
  _globals['_SHIP_ALIGNMENT']._serialized_start=311
  _globals['_SHIP_ALIGNMENT']._serialized_end=363
  _globals['_SHIP_CLASS']._serialized_start=366
  _globals['_SHIP_CLASS']._serialized_end=494
  _globals['_SERVICE']._serialized_start=496
  _globals['_SERVICE']._serialized_end=537
# @@protoc_insertion_point(module_scope)
