import asyncio
import pytest

from ocaapi.db import get_collection,connect_to_mongo,close_mongo_connection

@pytest.fixture(scope="session")
def event_loop():
    """Create a session-wide event loop."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

async def connect_to_database():
    print("🌐 Connecting to the database...")
    await connect_to_mongo()
    # await asyncio.sleep(0.1)  # simulate async connection

@pytest.fixture(scope="session", autouse=True)
async def before_all(event_loop):
    await connect_to_database()
    print("✅ Database connected before tests")
    yield 
    print("🔌 Disconnecting from database...")
    await close_mongo_connection()