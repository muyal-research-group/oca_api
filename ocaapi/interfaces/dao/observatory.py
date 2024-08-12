from pymongo.collection import Collection
from pymongo.results import DeleteResult
from pydantic import BaseModel
from option import NONE, Option,Some,Result,Ok,Err
from typing import Union,List,Any
import json as J
import string as S
from nanoid import generate as nanoid
from ocaapi.interfaces.dto.observatory import ObservatoryDTO,LevelCatalogDTO
from ocaapi.utils.utils import Utils as U
# def check_string(s):
#     s_len = len(s)
#     return s.isalnum() and (s_len >=18 and s_len <=32)

class LevelCatalog(BaseModel):
    level: int
    cid: str

class Observatory(BaseModel):
    obid:str=""
    title: str="Observatory"
    image_url:str=""
    description:str=""
    catalogs:List[LevelCatalog]=[]
    disabled:bool = False

class ObservatoryDAO(object):

    def __init__(self,collection:Collection):
        self.collection = collection

    def update_catalogs(self,obid:str,catalogs:List[LevelCatalog]=[])->Result[str,Exception]:
        try:
            _catalogs = list(map(lambda x: x.model_dump() , catalogs))
            result= self.collection.update_one({
                "obid":obid
            }, {
                "$set":{"catalogs": _catalogs  }
            })
            print(result)
            return Ok(obid)
        except Exception as e:
            return Err(e)
        
    def create(self,observatory:Observatory)->Result[str, Exception]:
        try:
            if observatory.obid == "":
                observatory.obid = nanoid(alphabet=S.ascii_lowercase+S.digits,size=24)
            if not U.check_string(observatory.obid):
                return Err(Exception("Obid({}) is not valid".format(observatory.obid)))
            db_res = self.collection.insert_one(observatory.model_dump())
            return Ok(observatory.obid)
        except Exception as e:
            return Err(e)

    def find_all(self,query:Any={},skip:int=0, limit:int = 10)->List[ObservatoryDTO]:
        cursor       = self.collection.find(query).skip(skip=skip).limit(limit=limit)
        result = []
        for observatory in cursor:
            del observatory["_id"]
            result.append(ObservatoryDTO(
                obid= observatory["obid"],
                title = observatory["title"],
                image_url= observatory.get("image_url",""),
                description = observatory.get("description","..."),
                catalogs= list ( map(lambda x: LevelCatalogDTO(**x),observatory["catalogs"]))
            ))
        cursor.close()
        return result
    def find_by_obid(self,obid:str)->Option[ObservatoryDTO]:
        res = self.collection.find_one({"obid":obid})
        if res:
            del res["_id"]
            return Some(
                ObservatoryDTO(
                    obid=res.get("obid","KEY"),
                    title=res.get("title","Titulo del Observatorio"),
                    image_url=res.get("image_url",""),
                    catalogs=list(map(lambda x: LevelCatalog(**x),res.get("catalogs",[]))),
                    description=res.get("description","Sin descripción por el momento."),
                )
            )
        else:
            return NONE

    def delete_by_obid(self,obid:str)->DeleteResult:
        return self.collection.delete_one({"obid": obid})
