from pymongo.collection import Collection
from pymongo.results import DeleteResult
from pydantic import BaseModel
from uuid import uuid4
from option import Option, NONE, Some
from typing import Dict,Union,List
from interfaces.dto.catalog import CatalogDTO,CatalogItemDTO
import json as J
from bson.json_util import dumps

class CatalogItem(BaseModel):
    name:str
    display_name:str
    code:str
    description:str
    metadata:Dict[str,str]

class Catalog(BaseModel):
    key:Union[str,None] = "catalog-{}".format(uuid4().hex)
    name:str
    display_name:str
    items: List[CatalogItem]

class CatalogDAO(object):

    def __init__(self,collection:Collection):
        self.collection = collection

    def create(self,catalog:CatalogDTO):
        # catalog.key = uuid4().hex
        self.collection.insert_one(catalog.model_dump())

    def find_all(self,skip:int=0, limit:int = 10)->List[CatalogDTO]:
        cursor      = self.collection.find({}).skip(skip=skip).limit(limit=limit)
        documents = []
        for document in cursor:
            del document["_id"]
            documents.append(CatalogDTO(
                key=document["key"],
                name= document["name"],
                display_name= document["display_name"],
                items= list( map(lambda x: CatalogItemDTO(**x), document["items"]) )
            ))

        cursor.close()
        return documents

    def find_by_key(self,key:str)->Option[CatalogDTO]:
        res = self.collection.find_one({"key":key})
        if res:
            del res["_id"]
            return Some(CatalogDTO(**res))
        else:
            return NONE

    def delete(self,key:str)->DeleteResult:
        return self.collection.delete_one({"key": key})
