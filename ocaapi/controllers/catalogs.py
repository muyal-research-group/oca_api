import os
import time as T
from typing import List
from fastapi import APIRouter,Depends
from fastapi import Response,HTTPException
from ocaapi.dto.catalog import CatalogDTO
from ocaapi.services import CatalogsService
# 
from ocaapi.repositories.catalog import CatalogsRepository
from ocaapi.db import get_collection
from ocaapi.services import CatalogsService
from ocaapi.log.log import Log
LOG_DEBUG = bool(int(os.environ.get("LOG_DEBUG","1")))
log = Log(
    name=os.environ.get("CATALOGS_LOG_NAME","oca_catalogs"),
    path=os.environ.get("LOG_OUTPUT_PATH","./log"),
    console_handler_filter= lambda x : LOG_DEBUG
)

router = APIRouter()


def get_service()->CatalogsService:
    collection =  get_collection(name="catalogs")
    repository = CatalogsRepository(collection= collection)
    service = CatalogsService(repository= repository)
    return service



@router.post("/catalogs")
async def create_catalogs(
    catalog:CatalogDTO, 
    catalog_service:CatalogsService= Depends(get_service) 
):
    start_time = T.time()

    exists = await catalog_service.find_by_cid(cid=catalog.cid)
    if exists.is_ok:
        raise HTTPException(
            status_code=409,
            detail=f"Catalog(cid={catalog.cid}) already exists."
        )
    
    res = await catalog_service.create(catalog=catalog)
    
    if res.is_err:
        error = res.unwrap_err()
        log.error({
            "msg":str(error)
        })
        raise HTTPException(status_code=500, detail="Catalog creation failed: {}".format(error))
    log.info({
        "event":"CREATE.CATALOG",
        "exists":exists.is_ok,
        "cid":catalog.cid,
        "display_name":catalog.display_name,
        "kind":catalog.kind,
        "response_time":T.time()-start_time
    })
    return { "cid": catalog.cid}


@router.delete("/catalogs/{cid}")
async def delete_catalogs(cid:str, catalog_service:CatalogsService= Depends(get_service)):
    exists = await catalog_service.find_by_cid(cid=cid)
    if  exists.is_err:
        return Response(content="Catalog(key={}) not found.".format(cid), status_code=403)
    else:
        response =await catalog_service.delete_by_cid(cid=cid)
        return Response(content=None, status_code=204)

@router.get("/catalogs")
async def get_catalogs(skip:int = 0, limit:int = 10, catalog_service:CatalogsService= Depends(get_service)):
    result= await catalog_service.find_all(skip=skip,limit=limit)
    if result.is_ok:
        return result.unwrap_or([])
    raise HTTPException(status_code=500, detail=str(result.unwrap_err()))

@router.get("/catalogs/{cid}")
async def get_catalogs_by_key(cid:str, catalog_service:CatalogsService= Depends(get_service)):
    catalog       =await catalog_service.find_by_cid(cid=cid)
    print(catalog)
    if catalog.is_err:
        raise HTTPException(detail="Catalog(key={}) not found".format(cid), status_code=404)
    return catalog.unwrap()

