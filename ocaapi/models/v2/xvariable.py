from pydantic import BaseModel, field_validator
from typing import Optional,Any,Dict
from enum import Enum
from datetime import datetime

class XVariableType(str,Enum):
    Spatial     = "SPATIAL"
    Temporal    = "TEMPORAL"
    Interest    = "INTEREST"
    Observable  = "OBSERVABLE"
    ProductType = "PRODUCT_TYPE"
    Info        = "INFO"

class XType(str, Enum):
    X                = "X"
    Integer          = "INTEGER"
    Float            = "FLOAT"
    String           = "STRING"
    IntegerRange     = "INTEGER_RANGE"
    Range            = "RANGE"
    Date             = "DATE"
    DateRange        = "DATE_RANGE"
    Array            = "ARRAY"
    Object           = "OBJECT"
    CategoricalRange = "CAT_RANGE"
    # Sequence     = "SEQUENCE"



class DataRangeX(BaseModel):
    end: datetime
    start: datetime
    left_open: Optional[bool]=False
    right_open:Optional[bool] = False

class PositiveIntRange(BaseModel):
    start: int
    end: int
    interval: int
    inclusive: bool 
    
class Range(BaseModel):
    start: float
    end: float
    interval: float
    inclusive: bool 

def check_datarange(v:Dict[Any,Any]):
    try:
        y = DataRangeX(**v)
        return True
    except Exception as e:
        return False


class XVariableParentRelationshipModel(BaseModel):
    parent_id: str
    child_id: str

class XVariableModel(BaseModel):
    xvid:Optional[str]=""
    description:Optional[str]=""
    type: str
    xtype:Optional[XType] = XType.X
    variable_type: Optional[XVariableType] = None
    raw: Optional[str] =""
    order: Optional[int]= -1
    value: Any
    
    @field_validator("value")
    def validate_value(cls, v, values):
        variable_type = values.data.get("variable_type")
        type          = values.data.get("type")
        if type == "DateRange":
            valid = check_datarange(v = v)
            if not valid:
                raise ValueError(f"Value must be a DataRangeX for the type: [{type}]")
            return v
        elif type == "Date":
            if not isinstance(v, datetime):
                raise ValueError(f"Value must be a datetime for the type: [{type}]")
            return v
        else:
            return v 
        
        

        
    # kind: str