from pymongo.collection import Collection
from pymongo.results import DeleteResult
from bson import ObjectId
from pydantic import BaseModel,validator
from option import Option, NONE, Some,Result,Ok,Err
from typing import List,Any,Optional
from utils.utils import Utils as U

class InequalityFilter(BaseModel):
    gt: Optional[int] = None  # Greater than
    lt: Optional[int] = None  # Less than
    eq: Optional[int] = None  # Equal to

    @validator('*', pre=True, always=True)
    def empty_str_to_none(cls, v):
        return v if v != "" else None

class InterestFilter(BaseModel):
    # Allow either a simple value (str) or an inequality filter
    value: Optional[str] = None
    inequality: Optional[InequalityFilter] = None

    # Ensure either value or inequality is provided, but not both
    @validator('inequality', always=True)
    def check_exclusivity(cls, v, values):
        if v and values.get('value'):
            raise ValueError('Provide either a value or an inequality, not both')
        if not v and not values.get('value'):
            raise ValueError('Provide at least a value or an inequality')
        return v
    
class  TemporalFilter(BaseModel):
    low: int
    high: int

class SpatialFilter(BaseModel):
    country: str
    state: str
    municipality: str
    def make_regex(self):
        
        x = ""
        if self.country == "*":
            x+=".*"
        else:
            x+= self.country+"\\."
        
        if self.state == "*":
            x+=".*"
        else:
            x+= "{}".format(self.state)
        
        if self.municipality == "*":
            x+=".*"
        else:
            x+= "{}".format(self.municipality)
            
        return x.upper()
        # return "{}|{}|{}".format(self.country, self.state,self.municipality).upper()
        # x = "^"
        # if self.country =="*":
        #     x +=".*\\"
        # else:
        #     x += "{}".format(self.country)
        
        # if self.state =="*":
        #     x +="\\..*"
        # else:
        #     x += "\\.{}".format(self.state)
        # if self.municipality =="*":
        #     x +="\\.*"
        # else:
        #     x += "\\.{}".format(self.municipality)
        # return x.upper()
        

        # return "{}".format()



class ProductFilter(BaseModel):
    temporal: Optional[TemporalFilter] = None
    spatial: Optional[SpatialFilter] = None
    interest: List[InterestFilter]=[]

class Level(BaseModel):
    index:int
    cid:str
    value:str
    kind:str =""

class Product(BaseModel):
    pid:str=""
    description:str=""
    levels:List[Level]=[]
    product_type: str=""
    level_path:str=""
    profile:str=""
    product_name: str=""
    tags:List[str]=[]
    url:str = ""
    

class ProductDAO(object):

    def __init__(self,collection:Collection):
        self.collection = collection

    def create(self,product:Product)->Result[str,Exception]:
        try:
            self.collection.insert_one(product.model_dump())
            return Ok(product.pid)
        except Exception as e:
            return Err(e)
    def creates(self, products:List[Product])->Result[Any,Exception]:
        try:
            docs = map(lambda p: p.model_dump(), products)
            self.collection.insert_many(docs)
            return Ok(None)
        except Exception as e :
            return Err(e)
        

    def find_all(self,query:Any={},skip:int=0, limit:int = 10)->List[Product]:
        cursor      = self.collection.find(query).skip(skip=skip).limit(limit=limit)
        documents = []
        for document in cursor:
            del document["_id"]
            documents.append(document)

        cursor.close()
        return documents

    def find_by_pid(self,pid:str)->Option[Product]:
        res = self.collection.find_one({"pid":pid})
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
        pipeline = []
        tags = list(filter(lambda x: len(x) >0 , tags))
        levels = list(filter(lambda x: len(x) >0 , levels))
        # print("TAGS",tags)
        if not len(tags) ==0 :
            pipeline.append(
                    {
                        "$match":{
                            "tags":{
                                "$all":tags
                            }
                        }
                    }
            )

        pipeline+=[
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
            },
            {
                "$limit":limit
            }
        ]
        cursor = self.collection.aggregate(pipeline=pipeline)
        documents = []
        for document in cursor:
            documents.append(document["_id"])
        return documents
    def delete(self,pid:str)->DeleteResult:
        return self.collection.delete_one({"pid": pid})
