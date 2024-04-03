from pymongo.collection import Collection
from pymongo.results import DeleteResult
from pydantic import BaseModel
from uuid import uuid4
from option import Option, NONE, Some,Result,Err,Ok

from typing import Any,List,Dict
from interfaces.dto.catalog import CatalogDTO,CatalogItemDTO
from nanoid import generate as nanoid
import string as S
from utils.utils import Utils as U

class CatalogItem(BaseModel):
    value:str
    display_name:str
    code:int
    description:str
    metadata:Dict[str,str]

class Catalog(BaseModel):
    cid:str = ""
    display_name:str = ""
    items: List[CatalogItem] = []
    kind:str = ""

class CatalogDAO(object):

    def __init__(self,collection:Collection):
        self.collection = collection

    def create(self,catalog:Catalog)->Result[str,Exception]:
        try:
            if catalog.cid == "":
               catalog.cid = nanoid(alphabet=S.ascii_lowercase+S.digits)

            if not U.check_string(catalog.cid):
                return Err(Exception("Cid({}) is not valid".format(catalog.cid)))
            self.collection.insert_one(catalog.model_dump())
            return Ok(catalog)
        except Exception as e:
            return Err(e)

    def find_all(self,query:Any={},skip:int=0, limit:int = 10)->List[CatalogDTO]:
        cursor      = self.collection.find(query).skip(skip=skip).limit(limit=limit)
        documents = []
        for document in cursor:
            del document["_id"]
            documents.append(CatalogDTO(
                cid=document["cid"],
                # name= document["name"],
                display_name= document["display_name"],
                items= list( map(lambda x: CatalogItemDTO(**x), document["items"]) ),
                kind= document["kind"],
            ))

        cursor.close()
        return documents

    def find_by_cid(self,cid:str)->Option[CatalogDTO]:
        res = self.collection.find_one({"cid":cid})
        if res:
            del res["_id"]
            items = list(map(lambda x : CatalogItemDTO(**x), res.get("items",[])))
            return Some(CatalogDTO(
                cid=res.get("cid",""),
                display_name=res.get("display_name","DISPLAY_NAME"),
                items=items,
                kind=res.get("kind","KIND"),
            ))
        else:
            return NONE

    def delete(self,cid:str)->DeleteResult:
        return self.collection.delete_one({"cid": cid})
