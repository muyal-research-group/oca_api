import os
from motor.motor_asyncio import AsyncIOMotorClient,AsyncIOMotorCollection

MONGODB_URI = os.environ.get("MONGODB_URI","mongodb://oca:d22a75e9e729debc@localhost:27017/ocadb?authSource=admin")
# client                   = MongoClient(MONGODB_URI)
MONGO_DATABASE_NAME      = os.environ.get("MONGO_DATABASE_NAME","ocadb")
# Initialize MongoClient
client = None

# Get the MongoDB client and database instance
def get_database():
    global client
    return  client[MONGO_DATABASE_NAME] if client else None 

def get_collection(name:str)->AsyncIOMotorCollection:
    db =  get_database()
    return db[name] if not db is None else None 
# Startup event to initialize the MongoClient when the application starts
async def connect_to_mongo():
    global client
    client = AsyncIOMotorClient(MONGODB_URI)

# Shutdown event to close the MongoClient when the application shuts down
async def close_mongo_connection():
    global client
    client.close()