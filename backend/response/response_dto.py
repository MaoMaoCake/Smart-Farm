from typing import Optional, TypeVar, Generic
from pydantic import BaseModel

T = TypeVar('T')

class ResponseDto(Generic[T], BaseModel):
    successful: bool
    error_code: str
    message: str
    status_code: int
    data: Optional[T] = None


def get_response_status(message: Optional[str] = None, data: Optional[T] = None) -> ResponseDto:
    return ResponseDto(
        successful=True,
        error_code='00',
        message=message if message else 'Success',
        status_code=200,
        data=data
    )
