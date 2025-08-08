from ocaapi.repositories.products import ProductsRepository
from ocaapi.repositories.observatory import ObservatoriesRepository
from ocaapi.repositories.catalog import CatalogsRepository
from option import Result,Ok,Err
from ocaapi.dto.observatory import ObservatoryDTO,LevelCatalogDTO
from ocaapi.dto.product import ProductDTO
from ocaapi.dto import ProductFilter
from ocaapi.models import LevelCatalog, Observatory,Catalog,CatalogItem,Product,Level
from ocaapi.errors import OcaError,AlreadyExists,NotFound,UknownError
from  typing import List,Dict,Any
from ocaapi.dto.catalog import CatalogDTO
from bson import ObjectId




class CatalogsService:

    def __init__(self,
        repository:CatalogsRepository
    ):
        self.repository = repository
    async def create(self, catalog:CatalogDTO)->Result[str, OcaError]:
        try:
            model = Catalog(
                cid          = catalog.cid,
                display_name = catalog.display_name,
                items        = [ CatalogItem(**i.model_dump()) for i in catalog.items],
                kind         = catalog.kind,
            )
            x = await self.repository.create(
                catalog= model
            )
            if x.is_err:
                return Err(
                    UknownError(
                        detail=str(x.unwrap_err())
                    )
                )
            return x
        except Exception as e:
            return Err(e)
    async def find_by_cid(self,cid:str)->Result[CatalogDTO,OcaError]:
        try:
            x = await self.repository.find_by_cid(cid=cid)
            if x.is_none:
                return Err(NotFound(detail=f"Catalog(cid={cid}) not found.",))
            return Ok(x.unwrap())
        except Exception as e:
            return Err(e)
    async def find_all(self,query:Dict[str,Any]={},skip:int =0, limit:str=100)->Result[List[CatalogDTO], Exception]:
        try:
            xs = await self.repository.find_all(query=query, skip=skip, limit=limit)
            return Ok(xs)
        except Exception as e:
            return Err(e)
    async def delete_by_cid(self, cid:str)->Result[str, Exception]:
        try:
            x = await self.repository.delete_by_cid(cid=cid)
            return Ok(cid)
        except Exception as e:
            return Err(e)

    
    # async def create(self,observatory:)->Result[str,OcaError]:


class ObservatoriesService:

    def __init__(self,
        repository:ObservatoriesRepository
    ):
        self.repository = repository

    
    async def create(self,observatory:ObservatoryDTO)->Result[str,OcaError]:
        try:
            exists = await self.repository.find_by_obid(obid= observatory.obid)
            if exists.is_some:
                return Err(AlreadyExists(detail="Observatory(key={}) already exists.".format(observatory.key) ))
            observatory.image_url="https://ivoice.live/wp-content/uploads/2019/12/no-image-1.jpg"
            model = Observatory(
                obid=observatory.obid,
                title= observatory.title,
                catalogs=observatory.catalogs,
                description=observatory.description,
                disabled=False,
                image_url= observatory.image_url
            )
            result = await self.repository.create(observatory=model)
            return result
        except Exception as e:
            return Err(e)
    
    async def update_catalogs(self, obid:str, catalogs: List[LevelCatalogDTO])->Result[str,OcaError]:
        try:
            xs = [ LevelCatalog(cid=i.cid, level=i.level) for i in catalogs]
            x = await self.repository.update_catalogs(
                obid= obid,
                catalogs= xs
            )
            return x
        except Exception as e:
            return Err(e)
        
    async def find_by_obid(self, obid:str)->Result[ObservatoryDTO,OcaError]:
        try:
            x = await self.repository.find_by_obid(obid=obid)
            if x.is_none:
                return Err(NotFound(detail="Observatory not found."))
            
            return Ok(x.unwrap())

        except Exception as e:
            return Err(e)
        
    async def find_all(self,query:Dict[str,Any] = {}, skip:int =0, limit:int =0 )->List[ObservatoryDTO]:
        return await self.repository.find_all(query=query,skip=skip,limit=limit)


class ProductsService:
    def __init__(
            self, 
            repository:ProductsRepository,
            observatory_service:ObservatoriesService,
            catalog_service:CatalogsService

    ):
        self.repository = repository
        self.observatory_service = observatory_service
        self.catalog_service = catalog_service
    
    async def create(self,product:ProductDTO)->Result[str, OcaError]:
        try:
            model = Product(
                description=product.description,
                level_path=product.level_path,
                levels=[ Level(**p.model_dump()) for p in product.levels],
                pid=product.pid,
                product_name=product.product_name,
                product_type=product.product_type,
                profile=product.profile,
                tags=product.tags,
                url=product.url
                # **product.model_dump()
            )
            x = await self.repository.create(product=model)
            if x.is_err:
                return Err(UknownError(detail="Product creation failed"))
            return Ok(product.pid)
        except Exception as e:
            return Err(e)
    async def create_many(self, products:List[ProductDTO]=[])->Result[List[str], OcaError]:
        try:
            xs = list(map(lambda x : Product(**x.model_dump()), products))
            res = await self.repository.creates(products=xs)
            if res.is_err:
                return Err(UknownError(detail="Products creation failed."))
            return Ok(list(map(lambda x :x.pid, products)))
        except Exception as e:
            return Err(e)
    async def find_by_pid(self, pid:str)->Result[ProductDTO, OcaError]:
        try:
            xs = await self.repository.find_by_pid(pid=pid)
            if xs.is_none:
                return Err(NotFound(detail="Product not found."))
            return Ok(xs.unwrap())
        except Exception as e:
            return Err(UknownError(detail=str(e)))
    
    async def find_all(self, query:Dict[str,Any]={}, skip:int =0, limit:int = 100)->Result[List[ProductDTO], OcaError]:
        try:
            xs = await self.repository.find_all(query=query, skip=skip,limit=limit)
            return Ok(xs)
        except Exception as e:
            return Err(UknownError(detail=str(e)))
    async def find_all_by_ids(self, ids:List[ObjectId])->Result[List[ProductDTO],OcaError]:
        try:
            xs = await self.repository.find_all_by_ids(ids=ids)
            return Ok(xs)
        except Exception as e:
            return Err(UknownError(detail=str(e)))
    async def filter_by_levels(self,tags:List[str],levels:List[str],skip:int=0, limit:int=100)->Result[List[ObjectId], OcaError]:
        try:
            xs = await self.repository.filter_by_levels(tags=tags,levels=levels, skip=skip, limit=limit)
            return Ok(xs)
        except Exception as e:
            return Err(UknownError(detail=str(e)))
    async def delete_by_pid(self, pid:str)->Result[str, OcaError]:
        try:
            x = await self.repository.delete_by_pid(pid=pid)
            return Ok(pid)
        except Exception as e:
            return Err(UknownError(detail=str(e)))
    async def filter(
        self,
        obid:str,
        filters:ProductFilter,
        skip:int =0,
        limit:int = 100, 
    )->List[ProductDTO]:
        result = await self.observatory_service.find_by_obid(obid=obid)
        if result.is_err:
            error = result.unwrap_err()
            raise error
        observatory = result.unwrap()
        catalogs:List[CatalogDTO] = []
        for catalog in observatory.catalogs:
            _catalog = await self.catalog_service.find_by_cid(cid=catalog.cid)
            if _catalog.is_err:
                error = _catalog.unwrap_err()
                raise error
                # raise HTTPException(status_code=500, detail="Catalog(cid={}) not found".format(catalog.cid))
            c = _catalog.unwrap()
            catalogs.append(c)
        
        temporal_catalog = next(filter(lambda x: x.kind=="TEMPORAL", catalogs),None)
        spatial_catalog = next(filter(lambda x: x.kind=="SPATIAL", catalogs),None)
        interest_catlaog = next(filter(lambda x: x.kind=="INTEREST", catalogs),None)

        pipeline = []
        tags=filters.tags
        if not len(tags) ==0 :
            pipeline.append(
                    {
                        "tags":{
                            "$all":tags
                        }
                    }
            )
        temporal_vals= []


        if (not temporal_catalog == None) and  (not filters.temporal == None):
            for e in temporal_catalog.items:
                v = int(e.value)
                if v >= filters.temporal.low and v <= filters.temporal.high:
                    temporal_vals.append(str(v))
            temporal_match =    {
                        'levels': {
                            '$elemMatch': {
                                'kind': 'TEMPORAL',
                                'value': {'$in': temporal_vals}
                            }
                        }
            }
            pipeline.append(temporal_match)
        if (not spatial_catalog == None) and (not filters.spatial == None):

            spatial_regex = filters.spatial.make_regex()
            spatial_match = {
                "levels.value":{
                    "$regex":spatial_regex
                }
            }

            pipeline.append(spatial_match)
        # print(interest_catlaog)
        if (not interest_catlaog == None) and not (len(filters.interest) == 0):
            for interest in filters.interest:
                print("INTEREST",interest)
                if not interest.value  == None:
                    x = {
                        "levels":{
                            "$elemMatch":{
                                "kind":"INTEREST",
                                "value":{"$in":[interest.value]}
                            }
                        }
                    }
                    pipeline.append(x)
                if not interest.inequality == None:
                    x = {
                            "levels":{
                                "$elemMatch":{
                                    "kind":"INTEREST_NUMERIC",
                                    "value":{
                                        "$gt":str(interest.inequality.gt),
                                        "$lt":str(interest.inequality.lt)
                                    }
                                }
                            }
                    }
                    pipeline.append(x)

                    

        if len(pipeline) == 0:
            _pipeline = [{"$match":{}}]
        else:
            _pipeline = [
                {
                    "$match":{
                        "$and":pipeline
                    }
                }
            ]
        
        # print(jsonable_encoder(_pipeline))
        curosr =  self.repository.collection.aggregate(pipeline=_pipeline)
        documents = []
        async for document in curosr:
            del document["_id"]
            documents.append(ProductDTO(**document))
        return documents

    # from ocaapi.dto.observatory import ObservatoryDTO,LevelCatalogDTO
