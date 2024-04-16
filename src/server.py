import os
import time as T
from typing import List
from fastapi import FastAPI,Response,HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
from pymongo import MongoClient
from interfaces.dao.catalog import Catalog,CatalogDAO,CatalogDTO
from interfaces.dao.observatory import Observatory,ObservatoryDAO,LevelCatalog
from interfaces.dao.products import ProductDAO,Product,ProductFilter
from interfaces.dao.rating import RatingDAO,RatingDTO,Rating
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from log.log import Log


LOG_DEBUG = bool(int(os.environ.get("LOG_DEBUG","1")))
# print("LOG_DEBUG",LOG_DEBUG)
log = Log(
    name=os.environ.get("LOG_NAME","ocapi"),
    path=os.environ.get("LOG_OUTPUT_PATH","/log"),
    console_handler_filter= lambda x : LOG_DEBUG
)
title = os.environ.get("OPENAPI_TITLE","OCA - API")
openapi_version = os.environ.get("OPENAPI_VERSION","0.0.1")
openapi_summary = os.environ.get("OPENAPI_SUMMARY","This API enable the manipulation of observatories and catalogs")
openapi_description = os.environ.get("OPENAPI_DESCRIPTION","")
app = FastAPI(
      root_path=os.environ.get("OPENAPI_PREFIX","/ocapi"),
    title=title,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
def generate_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=title,
        version=openapi_version,
        summary=openapi_version,
        description=openapi_description,
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": os.environ.get("OPENAPI_LOGO","https://i.ibb.co/9vSnz09/android-chrome-192x192.png")
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema
app.openapi = generate_openapi
# .openapi()

ip_addr                  = os.environ.get("MONGO_IP_ADDR","localhost")
port                     = os.environ.get("MONGO_PORT",27017)
client                   = MongoClient(os.environ.get("MONGO_URI","mongodb://{}:{}/".format(ip_addr, port)))
MONGO_DATABASE_NAME      = os.environ.get("MONGO_DATABASE_NAME","oca")
db                       = client[MONGO_DATABASE_NAME]
catalog_dao              = CatalogDAO(collection=db["catalogs"])
observatory_dao          = ObservatoryDAO(collection= db["observatories"])
product_dao              = ProductDAO(collection=db["products"])
rating_dao               = RatingDAO(collection=db["ratings"])




# Observatories
@app.post("/observatories")
def create_observatory(observatory: Observatory):
    start_time = T.time()
    exists = observatory_dao.find_by_obid(obid= observatory.obid)
    if exists:
        return Response(content="Observatory(key={}) already exists.".format(observatory.key), status_code=403)
    observatory.image_url="https://ivoice.live/wp-content/uploads/2019/12/no-image-1.jpg"
    result = observatory_dao.create(observatory=observatory)
    if result.is_err:
        error = result.unwrap_err()
        raise HTTPException(
            status_code=400,
            detail="Observatory creation error: {}".format(error)
        )
    log.info({
        "event":"CREATE.OBSERVATORY",
        "obid":observatory.obid,
        "title":observatory.title,
        "response_time":T.time() - start_time
    })
    return { "obid": observatory.obid}



@app.delete("/observatories/{obid}")
def delete_observatory_by_obid(obid:str):
    exists = observatory_dao.find_by_obid(obid=obid)
    if exists.is_none:
        raise HTTPException(detail="Observatory(obid={}) not found.".format(obid), status_code=404)
    else:
        response = observatory_dao.delete_by_obid(obid=obid)
        return Response(content=None, status_code=204)


@app.post("/observatories/{obid}")
def update_catalogs_by_obid(obid:str, catalogs:List[LevelCatalog]=[]):
    if len(catalogs)==0:
        return Response(status_code=204)
    result = observatory_dao.update_catalogs(obid=obid,catalogs=catalogs)
    if result.is_err:
        raise HTTPException(status_code=500, detail="Update failted: {}".format(obid))
    return Response(status_code=204)


@app.get("/observatories")
def get_observatories(skip:int = 0, limit:int = 10):
    documents = observatory_dao.find_all(query={"disabled":False},skip=skip,limit=limit)
    return documents

@app.post("/observatories/rate")
def rating_observatory(rating:Rating):
    rating_dao.create(rating=rating)
    return Response(status_code=204,content=None)


@app.get("/observatories/{obid}")
def get_observatory_by_key(obid:str):
    # observatory       = observatories_collection.find_one({"key":key})
    observatory = observatory_dao.find_by_obid(obid=obid)
    if observatory.is_none:
        return Response(content="Observatory(key={}) not found".format(obid), status_code=404)
    return observatory.unwrap()

# _______________________________
@app.post("/catalogs")
def create_catalogs(catalog:Catalog):
    exists = catalog_dao.find_by_cid(cid=catalog.cid)
    log.debug({
        "event":"CREATE.CATALOG",
        "exists":exists.is_some,
        "cid":catalog.cid,
        "display_name":catalog.display_name,
        "kind":catalog.kind
    })
    if exists.is_some:
        return Response(content="Catalog(cid={}) already exists.".format(catalog.cid), status_code=403)
    res = catalog_dao.create(catalog=catalog)
    # print(res)
    if res.is_err:
        error = res.unwrap_err()
        log.error({
            "msg":str(error)
        })
        raise HTTPException(status_code=500, detail="Catalog creation failed: {}".format(error))
    return { "cid": catalog.cid}

@app.delete("/catalogs/{cid}")
def delete_catalogs(cid:str):
    exists = catalog_dao.find_by_cid(cid=cid)
    if not exists.is_some:
        return Response(content="Catalog(key={}) not found.".format(cid), status_code=403)
    else:
        response =catalog_dao.delete(cid=cid)
        return Response(content=None, status_code=204)

@app.get("/catalogs")
def get_catalogs(skip:int = 0, limit:int = 10):
    documents= catalog_dao.find_all(skip=skip,limit=limit)
    return documents

@app.get("/catalogs/{cid}")
def get_catalogs_by_key(cid:str):
    catalog       =catalog_dao.find_by_cid(cid=cid)
    if catalog.is_none:
        raise HTTPException(detail="Catalog(key={}) not found".format(cid), status_code=404)
    return catalog.unwrap()


# Products
@app.get("/products")
def get_products(skip:int =0, limit:int = 100):
    documents = product_dao.find_all(skip=skip,limit=limit)
    return documents

@app.get("/products/{pid}")
def get_products(pid:str):
    documents = product_dao.find_by_pid(pid=pid)
    if documents.is_none:
        raise HTTPException(status_code=404, detail="Product not found.")
    return documents.unwrap()

# @app.get("/products/filter")
# def filter_products(tags:str,levels:str, skip:int =0, limit:int = 100):
#     splitted_levels = levels.split(",")
#     _tags = tags.split(",")
#     result = product_dao.filter_by_levels(tags=_tags,levels=splitted_levels,skip=skip, limit=limit)
#     products = product_dao.find_all_by_ids(ids = result)
#     return products

@app.post("/observatories/{obid}/products/nid")
def get_products_by_filter(obid:str,filters:ProductFilter,skip:int =0, limit:int = 100):

    result = observatory_dao.find_by_obid(obid=obid)
    if result.is_none:
        raise HTTPException(
            detail="Observatory(obid={}) not found".format(obid),
            status_code=500
        )
    
    observatory = result.unwrap()
    catalogs:List[CatalogDTO] = []
    for catalog in observatory.catalogs:
        _catalog = catalog_dao.find_by_cid(cid=catalog.cid)
        if _catalog.is_none:
            raise HTTPException(status_code=500, detail="Catalog(cid={}) not found".format(catalog.cid))
        c = _catalog.unwrap()
        catalogs.append(c)
    
    print(filters)
    temporal_catalog = next(filter(lambda x: x.kind=="TEMPORAL", catalogs),None)
    spatial_catalog = next(filter(lambda x: x.kind=="SPATIAL", catalogs),None)
    interest_catlaog = next(filter(lambda x: x.kind=="INTEREST", catalogs),None)

    # print("TEMPORAL",temporal_catalog)
    pipeline = []
    temporal_vals= []
    if not temporal_catalog == None:
        for e in temporal_catalog.items:
            v = int(e.value)
            if v >= filters.temporal.low and v <= filters.temporal.high:
                # print("VALID",v)
                temporal_vals.append(str(v))
        temporal_match =    {
                # '$match': {
                    'levels': {
                        '$elemMatch': {
                            'kind': 'TEMPORAL',
                            'value': {'$in': temporal_vals}
                        }
                    }
                # }
        }
        pipeline.append(temporal_match)
    if not spatial_catalog == None:

        spatial_regex = filters.spatial.make_regex()
        spatial_match = {
            "levels.value":{
                "$regex":spatial_regex
            }
        }

        pipeline.append(spatial_match)
    print(interest_catlaog)
    if not interest_catlaog == None:
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
                    # "$match":{
                        "levels":{
                            "$elemMatch":{
                                "kind":"INTEREST_NUMERIC",
                                "value":{
                                    "$gt":str(interest.inequality.gt),
                                    "$lt":str(interest.inequality.lt)
                                }
                            }
                        }
                    # }
                }
                pipeline.append(x)

                
    _pipeline = [
        {
            "$match":{
                "$and":pipeline
            }
        }
    ]
    print(jsonable_encoder(_pipeline))
    curosr = product_dao.collection.aggregate(pipeline=_pipeline)
    documents = []
    for document in curosr:
        del document["_id"]
        documents.append(document)
    # print("SPATIAL",spatial_catalog)
    # print("INTEREST", interest_catlaog)
    # print(documents)
    return JSONResponse(
        content= jsonable_encoder(documents)
        # jsonable_encoder(documents)
    )
    # return Response(status_code=204,content=J)
    # splitted_levels = levels.split(",")
    # _tags = tags.split(",")
    # result = product_dao.filter_by_levels(tags=_tags,levels=splitted_levels,skip=skip, limit=limit)
    # products = product_dao.find_all_by_ids(ids = result)
    # return products

@app.post("/products")
def create_products(products:List[Product]):
    start_time = T.time()
    product_dao.creates(products=products)
    service_time = T.time() - start_time
    return Response(content=None,status_code=201,)



@app.delete("/products/{pid}")
def delete_product_by_pid(pid:str):
    exists = product_dao.find_by_pid(pid=pid)
    if exists.is_none:
        raise HTTPException(detail="Product(pid={}) not found.".format(pid), status_code=404)
    else:
        response = product_dao.delete(pid=pid)
        return Response(content=None, status_code=204)

if __name__ =="__main__":
    uvicorn.run(
        host=os.environ.get("IP_ADDR"), 
        port=int(os.environ.get("PORT","5000")),
        reload=bool(int(os.environ.get("REALOAD","1"))),
        app="server:app"
    )