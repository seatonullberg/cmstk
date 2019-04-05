# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: types.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='types.proto',
  package='lattice',
  syntax='proto3',
  serialized_pb=_b('\n\x0btypes.proto\x12\x07lattice\"L\n\tProtoAtom\x12\t\n\x01x\x18\x01 \x01(\x02\x12\t\n\x01y\x18\x02 \x01(\x02\x12\t\n\x01z\x18\x03 \x01(\x02\x12\x0e\n\x06radius\x18\x04 \x01(\x02\x12\x0e\n\x06symbol\x18\x05 \x01(\t\"1\n\x0cProtoLattice\x12!\n\x05\x61toms\x18\x01 \x03(\x0b\x32\x12.lattice.ProtoAtomb\x06proto3')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_PROTOATOM = _descriptor.Descriptor(
  name='ProtoAtom',
  full_name='lattice.ProtoAtom',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='x', full_name='lattice.ProtoAtom.x', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='y', full_name='lattice.ProtoAtom.y', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='z', full_name='lattice.ProtoAtom.z', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='radius', full_name='lattice.ProtoAtom.radius', index=3,
      number=4, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='symbol', full_name='lattice.ProtoAtom.symbol', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=24,
  serialized_end=100,
)


_PROTOLATTICE = _descriptor.Descriptor(
  name='ProtoLattice',
  full_name='lattice.ProtoLattice',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='atoms', full_name='lattice.ProtoLattice.atoms', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=102,
  serialized_end=151,
)

_PROTOLATTICE.fields_by_name['atoms'].message_type = _PROTOATOM
DESCRIPTOR.message_types_by_name['ProtoAtom'] = _PROTOATOM
DESCRIPTOR.message_types_by_name['ProtoLattice'] = _PROTOLATTICE

ProtoAtom = _reflection.GeneratedProtocolMessageType('ProtoAtom', (_message.Message,), dict(
  DESCRIPTOR = _PROTOATOM,
  __module__ = 'types_pb2'
  # @@protoc_insertion_point(class_scope:lattice.ProtoAtom)
  ))
_sym_db.RegisterMessage(ProtoAtom)

ProtoLattice = _reflection.GeneratedProtocolMessageType('ProtoLattice', (_message.Message,), dict(
  DESCRIPTOR = _PROTOLATTICE,
  __module__ = 'types_pb2'
  # @@protoc_insertion_point(class_scope:lattice.ProtoLattice)
  ))
_sym_db.RegisterMessage(ProtoLattice)


# @@protoc_insertion_point(module_scope)
