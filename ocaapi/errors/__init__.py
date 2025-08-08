from typing import Any, Dict
from typing_extensions import Annotated, Doc
from fastapi import HTTPException

class OcaError(HTTPException):
    def __init__(self, status_code: int, detail: Any = None, headers: Dict[str, str]  = None) -> None:
        super().__init__(status_code, detail, headers)

class UknownError(OcaError):
    def __init__(self,detail: Any = None, headers: Dict[str, str]  = None) -> None:
        super().__init__(500, detail, headers)

class NotFound(OcaError):
    def __init__(self,detail: Any = None, headers: Dict[str, str]  = None) -> None:
        super().__init__(404, detail, headers)

class AlreadyExists(OcaError):
    def __init__(self,detail: Any = None, headers: Dict[str, str] = None) -> None:
        super().__init__(403, detail, headers)