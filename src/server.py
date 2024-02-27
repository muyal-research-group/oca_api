import os
import time as T
from typing import List
from fastapi import FastAPI,Response
from fastapi.openapi.utils import get_openapi
from pymongo import MongoClient
from interfaces.dao.catalog import Catalog,CatalogDAO
from interfaces.dao.observatory import Observatory,ObservatoryDAO
from interfaces.dao.products import ProductDAO,Product
from interfaces.dao.rating import RatingDAO,RatingDTO,Rating
import uvicorn
from fastapi.middleware.cors import CORSMiddleware


title = os.environ.get("OPENAPI_TITLE","OCA - API")
openapi_version = os.environ.get("OPENAPI_VERSION","0.0.1")
openapi_summary = os.environ.get("OPENAPI_SUMMARY","This API enable the manipulation of observatories and catalogs")
openapi_description = os.environ.get("OPENAPI_DESCRIPTION","")
app = FastAPI(
      openapi_prefix=os.environ.get("OPENAPI_PREFIX","/ocapi"),
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
    exists = observatory_dao.find_by_key(key= observatory.key)
    if exists:
        return Response(content="Observatory(key={}) already exists.".format(observatory.key), status_code=403)
    observatory.image_url="https://ivoice.live/wp-content/uploads/2019/12/no-image-1.jpg"
    observatory_dao.create(observatory=observatory)
    return { "key": observatory.key}

@app.delete("/observatories/{key}")
def delete_observatory(key:str):
    exists = observatory_dao.find_by_key(key=key)
    if exists:
        return Response(content="Observatory(key={}) already exists.".format(key), status_code=403)
    else:
        response = observatory_dao.delete(key=key)
        print(response)
        return Response(content=None, status_code=204)

@app.get("/observatories")
def get_observatories(skip:int = 0, limit:int = 10):
    documents = observatory_dao.find_all(skip=skip,limit=limit)
    return documents

@app.post("/observatories/rate")
def rating_observatory(rating:Rating):
    rating_dao.create(rating=rating)
    return Response(status_code=204,content=None)


@app.get("/observatories/{key}")
def get_observatory_by_key(key:str):
    # observatory       = observatories_collection.find_one({"key":key})
    observatory = observatory_dao.find_by_key(key=key)
    if observatory.is_none:
        return Response(content="Observatory(key={}) not found".format(key), status_code=404)
    return observatory.unwrap()

# _______________________________
@app.post("/catalogs")
def create_catalogs(catalog:Catalog):
    exists = catalog_dao.find_by_key(key=catalog.key)
    if exists.is_some:
        return Response(content="Catalog(key={}) already exists.".format(catalog.key), status_code=403)
    catalog_dao.create(catalog=catalog)
    return { "key": catalog.key}

@app.delete("/catalogs/{key}")
def delete_catalogs(key:str):
    exists = catalog_dao.find_by_key(key=key)
    if not exists.is_some:
        return Response(content="Catalog(key={}) not found.".format(key), status_code=403)
    else:
        response =catalog_dao.delete(key=key)
        print(response)
        return Response(content=None, status_code=204)

@app.get("/catalogs")
def get_catalogs(skip:int = 0, limit:int = 10):
    documents= catalog_dao.find_all(skip=skip,limit=limit)
    return documents

@app.get("/catalogs/{key}")
def get_catalogs_by_key(key:str):
    catalog       =catalog_dao.find_by_key(key=key)
    if catalog.is_none:
        return Response(content="Catalog(key={}) not found".format(key), status_code=404)
    return catalog.unwrap()


# Products
@app.get("/products")
def get_products(skip:int =0, limit:int = 100):
    documents = product_dao.find_all(skip=skip,limit=limit)
    return documents
@app.get("/products/filter")
def get_products(tags:str,levels:str, skip:int =0, limit:int = 100):
    splitted_levels = levels.split(",")
    _tags = tags.split(",")
    result = product_dao.filter_by_levels(tags=_tags,levels=splitted_levels,skip=skip, limit=limit)
    products = product_dao.find_all_by_ids(ids = result)
    return products
    # return documents


@app.post("/products")
def create_products(products:List[Product]):
    start_time = T.time()
    product_dao.creates(products=products)
    service_time = T.time() - start_time
    return Response(content=None,status_code=201,)



if __name__ =="__main__":
    uvicorn.run(
        host=os.environ.get("IP_ADDR"), 
        port=int(os.environ.get("PORT","5000")),
        reload=bool(int(os.environ.get("REALOAD","1"))),
        app="server:app"
    )