# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: geometry.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x0egeometry.proto\x12\x08vlsirlol"\x1d\n\x05Point\x12\t\n\x01x\x18\x01 \x01(\x03\x12\t\n\x01y\x18\x02 \x01(\x03"/\n\x05Layer\x12\x0e\n\x06number\x18\x01 \x01(\x03\x12\x16\n\x0e\x61nother_number\x18\x02 \x01(\x03"-\n\rQualifiedName\x12\x0e\n\x06\x64omain\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t"\\\n\tRectangle\x12\x0b\n\x03net\x18\x01 \x01(\t\x12#\n\nlower_left\x18\x02 \x01(\x0b\x32\x0f.vlsirlol.Point\x12\r\n\x05width\x18\x03 \x01(\x03\x12\x0e\n\x06height\x18\x04 \x01(\x03"9\n\x07Polygon\x12\x0b\n\x03net\x18\x01 \x01(\t\x12!\n\x08vertices\x18\x02 \x03(\x0b\x32\x0f.vlsirlol.Point"}\n\rLayeredShapes\x12\x1e\n\x05layer\x18\x01 \x01(\x0b\x32\x0f.vlsirlol.Layer\x12\'\n\nrectangles\x18\x02 \x03(\x0b\x32\x13.vlsirlol.Rectangle\x12#\n\x08polygons\x18\x03 \x03(\x0b\x32\x11.vlsirlol.Polygon"\xa0\x01\n\x04\x43\x65ll\x12%\n\x04name\x18\x01 \x01(\x0b\x32\x17.vlsirlol.QualifiedName\x12\'\n\x06shapes\x18\x02 \x03(\x0b\x32\x17.vlsirlol.LayeredShapes\x12%\n\tinstances\x18\x03 \x03(\x0b\x32\x12.vlsirlol.Instance\x12\x0e\n\x06\x61uthor\x18\x64 \x01(\t\x12\x11\n\tcopyright\x18\x65 \x01(\t"\x8d\x01\n\x08Instance\x12\x0c\n\x04name\x18\x01 \x01(\t\x12*\n\tcell_name\x18\x03 \x01(\x0b\x32\x17.vlsirlol.QualifiedName\x12"\n\x1arotation_clockwise_degrees\x18\x04 \x01(\x05\x12#\n\nlower_left\x18\x05 \x01(\x0b\x32\x0f.vlsirlol.Point"S\n\x08Geometry\x12(\n\x0ctop_instance\x18\x01 \x01(\x0b\x32\x12.vlsirlol.Instance\x12\x1d\n\x05\x63\x65lls\x18\x02 \x03(\x0b\x32\x0e.vlsirlol.Cellb\x06proto3'
)


_POINT = DESCRIPTOR.message_types_by_name["Point"]
_LAYER = DESCRIPTOR.message_types_by_name["Layer"]
_QUALIFIEDNAME = DESCRIPTOR.message_types_by_name["QualifiedName"]
_RECTANGLE = DESCRIPTOR.message_types_by_name["Rectangle"]
_POLYGON = DESCRIPTOR.message_types_by_name["Polygon"]
_LAYEREDSHAPES = DESCRIPTOR.message_types_by_name["LayeredShapes"]
_CELL = DESCRIPTOR.message_types_by_name["Cell"]
_INSTANCE = DESCRIPTOR.message_types_by_name["Instance"]
_GEOMETRY = DESCRIPTOR.message_types_by_name["Geometry"]
Point = _reflection.GeneratedProtocolMessageType(
    "Point",
    (_message.Message,),
    {
        "DESCRIPTOR": _POINT,
        "__module__": "geometry_pb2"
        # @@protoc_insertion_point(class_scope:vlsirlol.Point)
    },
)
_sym_db.RegisterMessage(Point)

Layer = _reflection.GeneratedProtocolMessageType(
    "Layer",
    (_message.Message,),
    {
        "DESCRIPTOR": _LAYER,
        "__module__": "geometry_pb2"
        # @@protoc_insertion_point(class_scope:vlsirlol.Layer)
    },
)
_sym_db.RegisterMessage(Layer)

QualifiedName = _reflection.GeneratedProtocolMessageType(
    "QualifiedName",
    (_message.Message,),
    {
        "DESCRIPTOR": _QUALIFIEDNAME,
        "__module__": "geometry_pb2"
        # @@protoc_insertion_point(class_scope:vlsirlol.QualifiedName)
    },
)
_sym_db.RegisterMessage(QualifiedName)

Rectangle = _reflection.GeneratedProtocolMessageType(
    "Rectangle",
    (_message.Message,),
    {
        "DESCRIPTOR": _RECTANGLE,
        "__module__": "geometry_pb2"
        # @@protoc_insertion_point(class_scope:vlsirlol.Rectangle)
    },
)
_sym_db.RegisterMessage(Rectangle)

Polygon = _reflection.GeneratedProtocolMessageType(
    "Polygon",
    (_message.Message,),
    {
        "DESCRIPTOR": _POLYGON,
        "__module__": "geometry_pb2"
        # @@protoc_insertion_point(class_scope:vlsirlol.Polygon)
    },
)
_sym_db.RegisterMessage(Polygon)

LayeredShapes = _reflection.GeneratedProtocolMessageType(
    "LayeredShapes",
    (_message.Message,),
    {
        "DESCRIPTOR": _LAYEREDSHAPES,
        "__module__": "geometry_pb2"
        # @@protoc_insertion_point(class_scope:vlsirlol.LayeredShapes)
    },
)
_sym_db.RegisterMessage(LayeredShapes)

Cell = _reflection.GeneratedProtocolMessageType(
    "Cell",
    (_message.Message,),
    {
        "DESCRIPTOR": _CELL,
        "__module__": "geometry_pb2"
        # @@protoc_insertion_point(class_scope:vlsirlol.Cell)
    },
)
_sym_db.RegisterMessage(Cell)

Instance = _reflection.GeneratedProtocolMessageType(
    "Instance",
    (_message.Message,),
    {
        "DESCRIPTOR": _INSTANCE,
        "__module__": "geometry_pb2"
        # @@protoc_insertion_point(class_scope:vlsirlol.Instance)
    },
)
_sym_db.RegisterMessage(Instance)

Geometry = _reflection.GeneratedProtocolMessageType(
    "Geometry",
    (_message.Message,),
    {
        "DESCRIPTOR": _GEOMETRY,
        "__module__": "geometry_pb2"
        # @@protoc_insertion_point(class_scope:vlsirlol.Geometry)
    },
)
_sym_db.RegisterMessage(Geometry)

if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _POINT._serialized_start = 28
    _POINT._serialized_end = 57
    _LAYER._serialized_start = 59
    _LAYER._serialized_end = 106
    _QUALIFIEDNAME._serialized_start = 108
    _QUALIFIEDNAME._serialized_end = 153
    _RECTANGLE._serialized_start = 155
    _RECTANGLE._serialized_end = 247
    _POLYGON._serialized_start = 249
    _POLYGON._serialized_end = 306
    _LAYEREDSHAPES._serialized_start = 308
    _LAYEREDSHAPES._serialized_end = 433
    _CELL._serialized_start = 436
    _CELL._serialized_end = 596
    _INSTANCE._serialized_start = 599
    _INSTANCE._serialized_end = 740
    _GEOMETRY._serialized_start = 742
    _GEOMETRY._serialized_end = 825
# @@protoc_insertion_point(module_scope)
