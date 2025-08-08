import pytest
from ocaapi.repositories.observatory import ObservatoriesRepository
from ocaapi.dto.observatory import ObservatoryDTO,LevelCatalogDTO
from ocaapi.services import ObservatoriesService
from ocaapi.models import Observatory
from ocaapi.db import get_collection,connect_to_mongo
import requests as R
import requests as R

@pytest.fixture
async def observatories_service():
    """Fixture to setup the Observatories service and repository."""
    # Setup: Connect to MongoDB and get the collection
    _          = await connect_to_mongo()
    c          = get_collection(name="observatories")
    repository = ObservatoriesRepository(collection=c)
    service    = ObservatoriesService(repository=repository)
    # Return repository and service for use in tests
    return repository, service


@pytest.mark.asyncio
async def test_repository_delete_all(observatories_service):
    repository, _ =  observatories_service

    # Fetch all records and count them
    xs = await repository.find_all(query={})
    n = len(xs)

    # Delete all records
    i = 0
    for ob in xs:
        await repository.delete_by_obid(obid=ob.obid)
        i += 1

    assert n == i, "Not all observatories were deleted"


@pytest.mark.asyncio
async def test_repository_create(observatories_service):
    repository, _ =  observatories_service

    # Create a new observatory
    obs = Observatory(
        obid="repositorycreationobs",
        title="Test",
        catalogs=[],
        description="Some description",
        image_url=""
    )
    res = await repository.create(observatory=obs)
    print(res)
    assert res.is_ok, "Observatory creation failed"


@pytest.mark.asyncio
async def test_service_create(observatories_service):
    _, service = observatories_service

    # Create a new observatory using the service
    obs = ObservatoryDTO(
        obid="servicecreationobs",
        title="Test",
        catalogs=[],
        description="Some description",
        image_url=""
    )
    x = await service.create(observatory=obs)

    print(x)
    assert x.is_ok, "Service failed to create observatory"


@pytest.mark.asyncio
async def test_api_create():
    # Create a new observatory DTO
    obs = ObservatoryDTO(
        obid="apicreationobs",
        title="Test",
        catalogs=[],
        description="Some description",
        image_url=""
    )

    # Send POST request to the API endpoint
    res = R.post("http://localhost:5000/observatories", json=obs.model_dump())

    print(res)
    assert res.status_code == 200, "API request failed"


@pytest.mark.order(-1)
@pytest.mark.asyncio
async def test_repository_find_all(observatories_service):
    repository, _ = observatories_service
    # Fetch all observatories
    xs = await repository.find_all(query={})
    # Ensure there are observatories present
    assert len(xs) >= 3, "No observatories found"
