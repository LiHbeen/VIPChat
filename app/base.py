from enum import Enum

from pydantic import BaseModel


class Code(Enum):
    SUCCESS = 'success'
    FAIL = 'fail'


class ResponseModel(BaseModel):
    code: Code.value
    data: dict = {}
    message: str = ''
