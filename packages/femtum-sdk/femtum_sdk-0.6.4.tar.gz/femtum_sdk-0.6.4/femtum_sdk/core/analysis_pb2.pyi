import femtum_sdk.core.component_pb2 as _component_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class OpticalSpectralAnalyserSweepResultDtoArray(_message.Message):
    __slots__ = ("Items",)
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    Items: _containers.RepeatedCompositeFieldContainer[OpticalSpectralAnalyserSweepResultDto]
    def __init__(self, Items: _Optional[_Iterable[_Union[OpticalSpectralAnalyserSweepResultDto, _Mapping]]] = ...) -> None: ...

class OpticalSpectralAnalyserSweepResultDto(_message.Message):
    __slots__ = ("WavelengthsArray", "PowersArray", "Name", "Tags", "WaferName", "ReticleName", "DieName", "CircuitName", "Id")
    WAVELENGTHSARRAY_FIELD_NUMBER: _ClassVar[int]
    POWERSARRAY_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    WAFERNAME_FIELD_NUMBER: _ClassVar[int]
    RETICLENAME_FIELD_NUMBER: _ClassVar[int]
    DIENAME_FIELD_NUMBER: _ClassVar[int]
    CIRCUITNAME_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    WavelengthsArray: _containers.RepeatedScalarFieldContainer[float]
    PowersArray: _containers.RepeatedScalarFieldContainer[float]
    Name: str
    Tags: _containers.RepeatedCompositeFieldContainer[_component_pb2.TagDto]
    WaferName: str
    ReticleName: str
    DieName: str
    CircuitName: str
    Id: str
    def __init__(self, WavelengthsArray: _Optional[_Iterable[float]] = ..., PowersArray: _Optional[_Iterable[float]] = ..., Name: _Optional[str] = ..., Tags: _Optional[_Iterable[_Union[_component_pb2.TagDto, _Mapping]]] = ..., WaferName: _Optional[str] = ..., ReticleName: _Optional[str] = ..., DieName: _Optional[str] = ..., CircuitName: _Optional[str] = ..., Id: _Optional[str] = ...) -> None: ...

class FindResultDataRequestDto(_message.Message):
    __slots__ = ("Name", "WaferName", "ReticleName", "DieName", "CircuitName", "Tags")
    NAME_FIELD_NUMBER: _ClassVar[int]
    WAFERNAME_FIELD_NUMBER: _ClassVar[int]
    RETICLENAME_FIELD_NUMBER: _ClassVar[int]
    DIENAME_FIELD_NUMBER: _ClassVar[int]
    CIRCUITNAME_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    Name: str
    WaferName: str
    ReticleName: str
    DieName: str
    CircuitName: str
    Tags: _containers.RepeatedCompositeFieldContainer[_component_pb2.TagDto]
    def __init__(self, Name: _Optional[str] = ..., WaferName: _Optional[str] = ..., ReticleName: _Optional[str] = ..., DieName: _Optional[str] = ..., CircuitName: _Optional[str] = ..., Tags: _Optional[_Iterable[_Union[_component_pb2.TagDto, _Mapping]]] = ...) -> None: ...
