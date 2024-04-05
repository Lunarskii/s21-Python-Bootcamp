from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Request(_message.Message):
    __slots__ = ("coords",)
    COORDS_FIELD_NUMBER: _ClassVar[int]
    coords: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, coords: _Optional[_Iterable[float]] = ...) -> None: ...

class Reply(_message.Message):
    __slots__ = ("ships",)
    SHIPS_FIELD_NUMBER: _ClassVar[int]
    ships: _containers.RepeatedCompositeFieldContainer[Ship]
    def __init__(self, ships: _Optional[_Iterable[_Union[Ship, _Mapping]]] = ...) -> None: ...

class Ship(_message.Message):
    __slots__ = ("alignment", "name", "ship_class", "length", "crew_size", "armed", "officers")
    class Alignment(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        ALIGNMENT_ALLY: _ClassVar[Ship.Alignment]
        ALIGNMENT_ENEMY: _ClassVar[Ship.Alignment]
    ALIGNMENT_ALLY: Ship.Alignment
    ALIGNMENT_ENEMY: Ship.Alignment
    class Class(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        CLASS_CORVETTE: _ClassVar[Ship.Class]
        CLASS_FRIGATE: _ClassVar[Ship.Class]
        CLASS_CRUISER: _ClassVar[Ship.Class]
        CLASS_DESTROYER: _ClassVar[Ship.Class]
        CLASS_CARRIER: _ClassVar[Ship.Class]
        CLASS_DREADNOUGHT: _ClassVar[Ship.Class]
    CLASS_CORVETTE: Ship.Class
    CLASS_FRIGATE: Ship.Class
    CLASS_CRUISER: Ship.Class
    CLASS_DESTROYER: Ship.Class
    CLASS_CARRIER: Ship.Class
    CLASS_DREADNOUGHT: Ship.Class
    class Officer(_message.Message):
        __slots__ = ("first_name", "last_name", "rank")
        FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
        LAST_NAME_FIELD_NUMBER: _ClassVar[int]
        RANK_FIELD_NUMBER: _ClassVar[int]
        first_name: str
        last_name: str
        rank: str
        def __init__(self, first_name: _Optional[str] = ..., last_name: _Optional[str] = ..., rank: _Optional[str] = ...) -> None: ...
    ALIGNMENT_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SHIP_CLASS_FIELD_NUMBER: _ClassVar[int]
    LENGTH_FIELD_NUMBER: _ClassVar[int]
    CREW_SIZE_FIELD_NUMBER: _ClassVar[int]
    ARMED_FIELD_NUMBER: _ClassVar[int]
    OFFICERS_FIELD_NUMBER: _ClassVar[int]
    alignment: Ship.Alignment
    name: str
    ship_class: Ship.Class
    length: float
    crew_size: int
    armed: bool
    officers: _containers.RepeatedCompositeFieldContainer[Ship.Officer]
    def __init__(self, alignment: _Optional[_Union[Ship.Alignment, str]] = ..., name: _Optional[str] = ..., ship_class: _Optional[_Union[Ship.Class, str]] = ..., length: _Optional[float] = ..., crew_size: _Optional[int] = ..., armed: bool = ..., officers: _Optional[_Iterable[_Union[Ship.Officer, _Mapping]]] = ...) -> None: ...
