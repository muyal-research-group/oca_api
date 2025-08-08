from motor.motor_asyncio import AsyncIOMotorDatabase,AsyncIOMotorCollection
from bson import ObjectId

class BaseRepository:
    def __init__(self, collection:AsyncIOMotorCollection):
        self.collection = collection

    async def create(self, data: dict):
        result = await self.collection.insert_one(data)
        return str(result.inserted_id)

    async def get_all(self):
        return [doc async for doc in self.collection.find()]

    async def get_by_id(self, obj_id: str):
        return await self.collection.find_one({"_id": ObjectId(obj_id)})

    async def delete_all(self):
        return await self.collection.delete_many({})

# Extend repositories
class MetaCatalogRepository(BaseRepository): pass
class CatalogRepository(BaseRepository): pass
class CatalogRelationshipRepository(BaseRepository): pass
class MetaCatalogCatalogRepository(BaseRepository): pass
class XVariableRepository(BaseRepository): pass
class CatalogXVariableRepository(BaseRepository): pass
class XVariableParentRepository(BaseRepository): pass
