from ocaapi.models.v2 import XVariableAssignment, ProductModel,XVariableModel,ObservatoryModel
from ocaapi.dto.v2 import ObservatoryDTO,XVariableDTO,MultipleXVariableAssignmentDTO,ProductDTO,XVariableRawAssignmentDTO,XVariableAssignmentDTO
from motor.motor_asyncio import AsyncIOMotorCollection
from option import Result,Ok,Err
from nanoid import generate as nanoid
from typing import List,Dict,Any
import hashlib as H

class ObservatoriesRepository:
    def __init__(self, collection:AsyncIOMotorCollection):
        self.collection = collection
        
    async def create(self, observatory: ObservatoryModel)->Result[str, Exception]:
        # Code to insert observatory in the database
        try:
            x = await self.collection.insert_one(observatory.model_dump(by_alias=True))
            return Ok(observatory.obid)
        except Exception as e:
            return Err(e)

    async def find_by_obid(self, obid: str)->Result[ObservatoryDTO,Exception]:
        try:
            x = await self.collection.find_one({"obid":obid})
            if not x:
                return Err(Exception("Observatory not found"))
            del x["_id"]
            return ObservatoryDTO(**x)
        except Exception as  e:
            return Err(e)



class XVariablesRepository:

    def __init__(self, collection:AsyncIOMotorCollection):
        self.collection = collection
        self.alphabet = "0123456789abcdefghijklmnopqrst"
        self.size = 10

    async def create(self, variable: XVariableModel)->Result[str, Exception]:
        try:
            if variable.xvid =="":
                suffix        = nanoid(alphabet=self.alphabet,size=self.size)
                variable.xvid = f"xv-{suffix}"
            x = await self.collection.insert_one(variable.model_dump())
            return Ok(variable.xvid)
        except Exception as e:
            return Err(e)

    async def find_by_type_value(self,type:str, value:str)->Result[XVariableDTO,Exception]:
        try:
            x      = f"{type}{value}"
            hasher = H.sha256()
            hasher.update(x.encode("utf-8"))
            xvid   = hasher.hexdigest()
            doc    = await self.collection.find_one({"xvid": xvid})
            if x is None:
                return Err(Exception("XVariable not found."))
            del doc["_id"]
            return Ok(XVariableDTO(**doc))
        except Exception as e: 
            return Err(e)

    async def find_by_xvids(self,
        xvids:List[str]
        # type:str, 
        # values:List[str]=[]
    )->Result[List[XVariableDTO],Exception]:
        try:
       
            xs    = await self.collection.find({"xvid": {"$in": xvids}})
            docs = []
            async for x in xs:
                del x["_id"]
                docs.append(XVariableDTO(**x))
            return Ok(docs)
        except Exception as e: 
            return Err(e)
    
    async def find_by_xvid(self, xvid: str)->Result[XVariableModel, Exception]:
        try:
            x = await self.collection.find_one({"xvid": xvid})
            if x is None:
                return Err(Exception("XVariable not found."))
            return Ok(XVariableModel(**x))
        except Exception as e:
            return Err(e)
    async def exists_by_xvid(self,xvid:str)->bool:
        x = await self.find_by_xvid(xvid=xvid)
        return x.is_ok

class XVariableAssignmentRepository:

    def __init__(self, collection:AsyncIOMotorCollection):
        self.collection = collection

    async def create_many(self, xs:List[XVariableAssignment] )->Result[List[str], Exception]:
        try:
            x = await self.collection.insert_many([x.model_dump() for x in xs])
            res = list(map(lambda y: y.xid ,  xs))
            return Ok(res)
        except Exception as e:
            return Err(e)
        
    async def find_one_by_xvid(self,xvid:str)->Result[XVariableAssignmentDTO, Exception]:
        try:
            res = await self.collection.find_one({"xvid":xvid})
            if res is None:
                return Err(Exception("Xvarible Assignment not found"))
            del res["_id"]
            return Ok(XVariableAssignmentDTO(**res))
        except Exception as e:
            return Err(e)
    
    async def find(self,query:Dict[str, Any],skip:int= 0, limit:int = 100)->Result[List[XVariableAssignmentDTO], Exception]:
        try:
            res = self.collection.find(query).skip(skip=skip).limit(limit=limit)
            xs  = []
            async for x in res:
                del x["_id"]
                xs.append(XVariableAssignmentDTO(**x))
            return Ok(xs)
        except Exception as e:
            return Err(e)
    
    async def exists_by_xid_and_xvid(self,xid:str, xvid:str)->bool:
        try:
            x = await self.collection.find_one({"xid":xid, "xvid":xvid})
            return not (x is None)
        except Exception as e:
            return False
        
    async def create(self, x:XVariableAssignment )->Result[str, Exception]:
        try:
            res = await self.collection.insert_one(x.model_dump())
            return Ok(x.xid)
        except Exception as e:
            return Err(e)
    
 

class ProductRepository:

    def __init__(self, collection:AsyncIOMotorCollection):
        self.collection = collection

    async def create(self, product:ProductModel )->Result[str, Exception]:
        try:
            x = await self.collection.insert_one(product.model_dump())
            return Ok(product.pid)
        except Exception as e:
            return Err(e)
    async def find_all(self,query:Dict[str, Any]={},skip:int = 0, limit:int = 100)->Result[List[ProductDTO], Exception]:
        try:
            res = self.collection.find(query).skip(skip=skip).limit(limit=limit)
            xs = []
            async for x in res:
                del x["_id"]
                xs.append(ProductDTO(**x))
            return Ok(xs)
        except Exception as e:
            return Err(e)
    async def find_by_pid(self, pid:str)->Result[ProductDTO,Exception]:
        try:
            x = await self.collection.find_one({"pid": pid})
            if x is None:
                return Err(Exception("Product not found."))
            del x["_id"]
            return Ok(ProductDTO(**x))

        except Exception as e:
            return Err(e)
    async def exists_by_pid(self,pid:str)-> bool:
        x = await self.find_by_pid(pid=pid)
        return x.is_ok