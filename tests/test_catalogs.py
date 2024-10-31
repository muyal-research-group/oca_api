import pytest
from ocaapi.repositories.catalog import CatalogsRepository
from ocaapi.dto.catalog import CatalogDTO,CatalogItemDTO
from ocaapi.services import CatalogsService
from ocaapi.models import Catalog,CatalogKind
from ocaapi.db import get_collection,connect_to_mongo
import requests as R
import requests as R

@pytest.fixture
async def catalog_service():
    """Fixture to setup the Catalog service and repository."""
    # Setup: Connect to MongoDB and get the collection
    _          = await connect_to_mongo()
    c          = get_collection(name="catalogs")
    repository = CatalogsRepository(collection=c)
    service    = CatalogsService(repository=repository)
    # Return repository and service for use in tests
    return repository, service


@pytest.mark.asyncio
async def test_repository_delete_all(catalog_service):
    repository, _ =  catalog_service

    # Fetch all records and count them
    xs = await repository.find_all(query={})
    n = len(xs)

    # Delete all records
    i = 0
    for ob in xs:
        await repository.delete_by_cid(cid = ob.cid)
        i += 1

    assert n == i, "Not all observatories were deleted"


@pytest.mark.asyncio
async def test_repository_create(catalog_service):
    repository, _ =  catalog_service

    # Create a new observatory
    obs = Catalog(
        cid          = "repositorycatalogcid",
        display_name = "Catalog - Reposiroty",
        items        = [],
        kind         = CatalogKind.INTEREST
    )
    res = await repository.create(catalog=obs)
    print(res)
    assert res.is_ok, "Catalog creation failed"


@pytest.mark.asyncio
async def test_service_create(catalog_service):
    _, service = catalog_service

    # Create a new observatory using the service
    obs = CatalogDTO(
        cid          = "servicecatalogcid",
        display_name = "Catalog - Reposiroty",
        items        = [],
        kind         = CatalogKind.INTEREST
    )
    x = await service.create(catalog=obs)

    print(x)
    assert x.is_ok, "Service failed to create catalog"


@pytest.mark.asyncio
async def test_api_create():
    # Create a new observatory DTO
    obs = CatalogDTO(
        cid          = "apicatalogcid",
        display_name = "Catalog - Reposiroty",
        items        = [],
        kind         = CatalogKind.INTEREST
    )
    # Send POST request to the API endpoint
    res = R.post("http://localhost:5000/catalogs", json=obs.model_dump())

    print(res)
    assert res.status_code == 200, "API request failed"


@pytest.mark.order(-1)
@pytest.mark.asyncio
async def test_repository_find_all(catalog_service):
    repository, _ = catalog_service
    # Fetch all observatories
    xs = await repository.find_all(query={})
    # Ensure there are observatories present
    assert len(xs) >= 3, "No observatories found"
