import pytest
from ocaapi.repositories.v2 import ObservatoriesRepository
from ocaapi.dto.v2 import ObservatoryDTO
from ocaapi.services.v2 import ObservatoriesService
from ocaapi.models.v2 import ObservatoryModel
from ocaapi.db import get_collection,connect_to_mongo
import requests as R

@pytest.fixture
async def observatories_service():
    """Fixture to setup the Observatories service and repository."""
    # Setup: Connect to MongoDB and get the collection
    _          = await connect_to_mongo()
    c          = get_collection(name="observatoriesv2")
    repository = ObservatoriesRepository(collection=c)
    service    = ObservatoriesService(repo=repository)
    # Return repository and service for use in tests
    return repository, service



@pytest.mark.asyncio
async def test_repository_create(observatories_service):
    repository, _ =  observatories_service
    # Create a new observatory
    obs = ObservatoryModel(
        obid="repositorycreationobs",
        title="Test",
        description="Some description",
    )
    res = await repository.create(observatory=obs)
    print(res)
    assert res.is_ok, "Observatory creation failed"

@pytest.mark.asyncio
async def test_service_create(observatories_service):
    _,service =  observatories_service
    # Create a new observatory
    obs = ObservatoryDTO(
        obid="servicecreationobs",
        title="TestService",
        description="Some description service",
    )
    res = await service.create(observatory=obs)
    print(res)
    assert res.is_ok, "Observatory creation failed"