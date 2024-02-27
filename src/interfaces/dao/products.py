from pymongo.collection import Collection
from pymongo.results import DeleteResult
from bson import ObjectId
from pydantic import BaseModel
from uuid import uuid4
from option import Option, NONE, Some
from typing import Dict,Union,List
from interfaces.dto.catalog import CatalogDTO,CatalogItemDTO
import json as J
from bson.json_util import dumps

# class CatalogItem(BaseModel):
#     name:str
#     display_name:str
#     code:str
#     description:str
#     metadata:Dict[str,str]


class Level(BaseModel):
    index:int
    catalog_id:str
    value:str

class Product(BaseModel):
    key:str=""
    description:str=""
    levels:List[Level]=[]
    product_type: str=""
    kind: str=""
    level_index:int=-1
    level_path:str=""
    profile:str=""
    product_name: str=""
    spatial:str=""
    temporal:str=""
    interest:List[str]=[]
    tags:List[str]=[]
    pid:str ="PRODUCT_ID"
    

class ProductDAO(object):

    def __init__(self,collection:Collection):
        self.collection = collection

    def create(self,product:Product):
        self.collection.insert_one(product.model_dump())
    def creates(self, products:List[Product]):
        docs = map(lambda p: p.model_dump(), products)
        self.collection.insert_many(docs)
        

    def find_all(self,skip:int=0, limit:int = 10)->List[Product]:
        cursor      = self.collection.find({}).skip(skip=skip).limit(limit=limit)
        documents = []
        for document in cursor:
            del document["_id"]
            documents.append(document)
            # documents.append(CatalogDTO(
            #     key=document["key"],
            #     name= document["name"],
            #     display_name= document["display_name"],
            #     items= list( map(lambda x: CatalogItemDTO(**x), document["items"]) )
            # ))

        cursor.close()
        return documents

    def find_by_key(self,key:str)->Option[Product]:
        res = self.collection.find_one({"key":key})
        if res:
            del res["_id"]
            return Some(Product(**res))
            # return Some(CatalogDTO(**res))
        else:
            return NONE
    def find_all_by_ids(self,ids:List[ObjectId]):
        cursor = self.collection.find({"_id":{"$in":ids}})
        documents=[]
        for document in cursor:
            del document["_id"]
            documents.append(document)
        return documents
    def filter_by_levels(self,tags:List[str],levels:List[str],skip:int, limit:int):
        cursor = self.collection.aggregate([
        {
            "$match":{
                "tags":{
                    "$all":tags
                }
            }
        },
        {
            "$unwind": "$levels"
        },
        {
            "$group": {
            "_id": "$_id",
            "values":{"$addToSet":"$levels.value"}
            }
        },
        { "$match": { "values":{"$all":levels }}},
        {
                "$project": {
                    "_id": 1
                }
        },
        {
            "$skip":skip,
        },{
            "$limit":limit
            }
        ])
        documents = []
        for document in cursor:
            documents.append(document["_id"])
        return documents
    def delete(self,key:str)->DeleteResult:
        return self.collection.delete_one({"key": key})
