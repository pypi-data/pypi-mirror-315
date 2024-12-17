from com.hayatapps.pa.model import paservice_request_pb2 as _paservice_request_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PAServiceRequestRq(_message.Message):
    __slots__ = ("serviceRequest",)
    SERVICEREQUEST_FIELD_NUMBER: _ClassVar[int]
    serviceRequest: _paservice_request_pb2.PAServiceRequest
    def __init__(self, serviceRequest: _Optional[_Union[_paservice_request_pb2.PAServiceRequest, _Mapping]] = ...) -> None: ...

class PAServiceRequestRs(_message.Message):
    __slots__ = ("serviceRequest",)
    SERVICEREQUEST_FIELD_NUMBER: _ClassVar[int]
    serviceRequest: _paservice_request_pb2.PAServiceRequest
    def __init__(self, serviceRequest: _Optional[_Union[_paservice_request_pb2.PAServiceRequest, _Mapping]] = ...) -> None: ...
