# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: netlist.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import circuit_pb2 as circuit__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\rnetlist.proto\x12\rvlsir.netlist\x1a\rcircuit.proto"\x89\x01\n\x0cNetlistInput\x12#\n\x03pkg\x18\x01 \x01(\x0b\x32\x16.vlsir.circuit.Package\x12\x14\n\x0cnetlist_path\x18\x02 \x01(\t\x12)\n\x03\x66mt\x18\x03 \x01(\x0e\x32\x1c.vlsir.netlist.NetlistFormat\x12\x13\n\x0bresult_path\x18\x04 \x01(\t"=\n\rNetlistResult\x12\x11\n\x07success\x18\x01 \x01(\x08H\x00\x12\x0e\n\x04\x66\x61il\x18\x02 \x01(\tH\x00\x42\t\n\x07variant*q\n\rNetlistFormat\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07SPECTRE\x10\x01\x12\t\n\x05SPICE\x10\x02\x12\x0b\n\x07NGSPICE\x10\x03\x12\x08\n\x04XYCE\x10\x04\x12\n\n\x06HSPICE\x10\x05\x12\x07\n\x03\x43\x44L\x10\x06\x12\x0b\n\x07VERILOG\x10\n2O\n\x07Netlist\x12\x44\n\x07Netlist\x12\x1b.vlsir.netlist.NetlistInput\x1a\x1c.vlsir.netlist.NetlistResultb\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "netlist_pb2", _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    DESCRIPTOR._loaded_options = None
    _globals["_NETLISTFORMAT"]._serialized_start = 250
    _globals["_NETLISTFORMAT"]._serialized_end = 363
    _globals["_NETLISTINPUT"]._serialized_start = 48
    _globals["_NETLISTINPUT"]._serialized_end = 185
    _globals["_NETLISTRESULT"]._serialized_start = 187
    _globals["_NETLISTRESULT"]._serialized_end = 248
    _globals["_NETLIST"]._serialized_start = 365
    _globals["_NETLIST"]._serialized_end = 444
# @@protoc_insertion_point(module_scope)
