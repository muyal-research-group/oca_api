from pydantic import BaseModel
from ocaapi.repositories.v3 import BaseRepository

class BaseService:
    def __init__(self, repository:BaseRepository):
        self.repository = repository

    async def create(self, model: BaseModel):
        return await self.repository.create(model.model_dump(by_alias=True))

    async def get_all(self):
        xs = await self.repository.get_all()
        for x in xs:
            del x["_id"]

        return xs

    async def get_by_id(self, obj_id: str):
        return await self.repository.get_by_id(obj_id)

class MetaCatalogService(BaseService): pass
class CatalogService(BaseService): pass
class CatalogRelationshipService(BaseService): pass
class MetaCatalogCatalogService(BaseService): pass
class XVariableService(BaseService): pass
class CatalogXVariableService(BaseService): pass
class XVariableParentService(BaseService): pass