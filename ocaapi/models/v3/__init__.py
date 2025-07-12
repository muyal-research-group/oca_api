from pydantic import BaseModel, Field
from typing import List, Optional
import hashlib as H


from bson import ObjectId
from pydantic_core import core_schema
from pydantic import GetCoreSchemaHandler
from typing import Any
class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: Any, handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        return core_schema.no_info_plain_validator_function(cls.validate)

    @classmethod
    def validate(cls, v: Any) -> ObjectId:
        if isinstance(v, ObjectId):
            return v
        if isinstance(v, str) and ObjectId.is_valid(v):
            return ObjectId(v)
        raise ValueError(f"Invalid ObjectId: {v}")


class MetaCatalog(BaseModel):
    mcid:str
    name: str
    description: Optional[str] = None

# Catalog
class Catalog(BaseModel):
    cid:str
    name: str
    description: Optional[str] = None
    xtype: str

# CatalogRelationship
class CatalogRelationship(BaseModel):
    catalog_id: str
    parent_catalog_id: str
    order: Optional[int] = None

# MetaCatalogCatalog
class MetaCatalogCatalog(BaseModel):
    meta_catalog_id: str
    catalog_id: str
# XVariable
from enum import Enum
# Enum for XType
class XTypeEnum(str, Enum):
    SPATIAL = "SPATIAL"
    TEMPORAL = "TEMPORAL"
    INTEREST = "INTEREST"
    OBSERVABLE = "OBSERVABLE"

# Enum for VariableType
class VariableTypeEnum(str, Enum):
    INT = "INT"
    FLOAT = "FLOAT"
    STRING = "STRING"
    TUPLE = "TUPLE"
    LIST = "LIST"
    
class XVariable(BaseModel):
    xvid:str
    xtype: XTypeEnum
    value: str
    variable_type: VariableTypeEnum
    hash:Optional[str] = None
    def model_post_init(self, __context):
        if not self.hash:
            self.hash = H.sha256(self.value.encode()).hexdigest()

# CatalogXVariable
class CatalogXVariable(BaseModel):
    catalog_id: str
    xvariable_id: str

# XVariableParent
class XVariableParent(BaseModel):
    xvariable_id: str
    parent_xvariable_id: str
