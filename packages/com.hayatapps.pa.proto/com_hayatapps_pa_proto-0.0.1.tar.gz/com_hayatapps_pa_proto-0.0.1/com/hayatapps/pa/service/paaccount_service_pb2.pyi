from com.hayatapps.pa.model import paaccount_pb2 as _paaccount_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PAAccountRq(_message.Message):
    __slots__ = ("service",)
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    service: _paaccount_pb2.PAAccount
    def __init__(self, service: _Optional[_Union[_paaccount_pb2.PAAccount, _Mapping]] = ...) -> None: ...

class PAAccountRs(_message.Message):
    __slots__ = ("service",)
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    service: _paaccount_pb2.PAAccount
    def __init__(self, service: _Optional[_Union[_paaccount_pb2.PAAccount, _Mapping]] = ...) -> None: ...
