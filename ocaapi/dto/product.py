from pydantic import BaseModel
from ocaapi.models import CatalogKind
from typing import List,Optional

class LevelDTO(BaseModel):
    index:int
    cid:str
    value:str
    kind:CatalogKind
    
class ProductDTO(BaseModel):
    pid:str
    description:Optional[str]=""
    product_type:str    
    level_path:str  
    levels:List[LevelDTO]
    profile:str     
    product_name:str
    url:str
    tags:Optional[List[str]]=[]