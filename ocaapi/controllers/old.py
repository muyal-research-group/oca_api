# import os
# import time as T
# from typing import List
# from fastapi import APIRouter,Depends
# from fastapi import Response,HTTPException
# from fastapi.encoders import jsonable_encoder
# from fastapi.responses import JSONResponse
# # 
# from ocaapi.dto.observatory import ObservatoryDTO,LevelCatalogDTO
# from ocaapi.repositories.catalog import Catalog,CatalogDTO
# from ocaapi.repositories.observatory import ObservatoriesRepository
# from ocaapi.repositories.products import Product,ProductFilter
# from ocaapi.repositories.rating import Rating
# from ocaapi.db import get_collection
# from ocaapi.services import ObservatoriesService
# from ocaapi.log.log import Log
# LOG_DEBUG = bool(int(os.environ.get("LOG_DEBUG","1")))
# log = Log(
#     name=os.environ.get("LOG_NAME","ocapi"),
#     path=os.environ.get("LOG_OUTPUT_PATH","/log"),
#     console_handler_filter= lambda x : LOG_DEBUG
# )

# router = APIRouter()


# # def get_service()->ObservatoriesService:
# #     collection =  get_collection(name="continents")
# #     repository = ObservatoriesRepository(collection= collection)
# #     service = ObservatoriesService(repository= repository)
# #     return service




# # _______________________________
