from pymongo.collection import Collection
from pymongo.results import DeleteResult
from pydantic import BaseModel
from option import NONE, Option,Some
from bson.json_util import dumps
from typing import Union,List
from uuid import uuid4
import json as J
from interfaces.dto.observatory import ObservatoryDTO,LevelCatalogDTO

class LevelCatalog(BaseModel):
    level: int
    catalog_key: str

class Observatory(BaseModel):
    obid:str=""
    key:str
    title: str
    image_url:str=""
    description:str
    catalogs:List[LevelCatalog]

class ObservatoryDAO(object):

    def __init__(self,collection:Collection):
        self.collection = collection

    def create(self,observatory:Observatory):
        self.collection.insert_one(observatory.model_dump())

    def find_all(self,skip:int=0, limit:int = 10)->List[ObservatoryDTO]:
        cursor       = self.collection.find({}).skip(skip=skip).limit(limit=limit)
        result = []
        for observatory in cursor:
            del observatory["_id"]
            result.append(ObservatoryDTO(
                key= observatory["key"],
                title = observatory["title"],
                image_url= observatory.get("image_url",""),
                description = observatory.get("description","..."),
                catalogs= list ( map(lambda x: LevelCatalogDTO(**x),observatory["catalogs"]))
            ))
        cursor.close()
        return result

    def find_by_key(self,key:str)->Option[ObservatoryDTO]:
        res = self.collection.find_one({"key":key})
        if res:
            del res["_id"]
            return Some(
                ObservatoryDTO(
                    catalogs=res.get("catalogs"),
                    description=res.get("description","Sin descripción por el momento."),
                    image_url=res.get("image_url",""),
                    key=res.get("key","KEY"),
                    title=res.get("title","Titulo del Observatorio"),
                )
            )
        else:
            return NONE

    def delete(self,key:str)->DeleteResult:
        return self.collection.delete_one({"key": key})
