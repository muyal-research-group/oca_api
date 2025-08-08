from typing import Dict,Union,List,Optional,Any
from pydantic import BaseModel
class CatalogItemDTO(BaseModel):
    value:str         
    display_name:str
    code:int 
    description:str
    metadata:Optional[Dict[str,Any]]={}
    
class CatalogDTO(BaseModel):
    cid:Optional[str]=""
    display_name:str 
    items:Optional[List[CatalogItemDTO]]=[]
    kind:str