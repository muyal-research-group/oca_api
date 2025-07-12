import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from ocaapi.log.log import Log
from ocaapi.db import connect_to_mongo,close_mongo_connection
from ocaapi.controllers import observatories_router,catalogs_router,products_router,v3_router
from ocaapi.controllers.v2 import observatory_router_v2,xvariable_router,nameservice_router,product_router_v2


LOG_DEBUG = bool(int(os.environ.get("LOG_DEBUG","1")))
log = Log(
    name=os.environ.get("LOG_NAME","ocapi"),
    path=os.environ.get("LOG_OUTPUT_PATH","/log"),
    console_handler_filter= lambda x : LOG_DEBUG
)
title = os.environ.get("OPENAPI_TITLE","OCA - API")
openapi_version = os.environ.get("OPENAPI_VERSION","0.0.1")
openapi_summary = os.environ.get("OPENAPI_SUMMARY","This API enable the manipulation of observatories and catalogs")
openapi_description = os.environ.get("OPENAPI_DESCRIPTION","")

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield 
    await close_mongo_connection()

    
app = FastAPI(
    lifespan=lifespan,
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



app.include_router(observatories_router)
app.include_router(catalogs_router)
app.include_router(products_router)
app.include_router(observatory_router_v2)
app.include_router(xvariable_router)
app.include_router(nameservice_router)
app.include_router(product_router_v2)
app.include_router(v3_router)