from pydantic import BaseModel
from enum import Enum

class CatalogType(str,Enum):
    Dropdown     = "DROPDOWN"
    Date         = "DATE"
    DateRange    = "DATE_RANGE"
    IntegerRange = "INTEGER_RANGE"
    FloatRange   = "FLOAT_RANGE"
    Integer      = "INTEGER"
    Float        = "FLOAT"

class CatalogModel(BaseModel):
    cid: str 
    name: str
    description: str
    type: CatalogType

class CatalogXVariableRelation(BaseModel):
    cid:str
    xvid: str