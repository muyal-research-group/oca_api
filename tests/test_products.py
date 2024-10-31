import pytest

from ocaapi.repositories.observatory import ObservatoriesRepository
from ocaapi.repositories.products import ProductsRepository
from ocaapi.repositories.catalog import CatalogsRepository
from ocaapi.services import ProductsService,ObservatoriesService,CatalogsService
from ocaapi.models import Observatory,Product,CatalogKind,Level
from ocaapi.dto import ProductFilter
from ocaapi.dto.product import ProductDTO,LevelDTO
from ocaapi.db import get_collection,connect_to_mongo
import requests as R

@pytest.fixture
async def products_service():
    """Fixture to setup the Observatories service and repository."""
    # Setup: Connect to MongoDB and get the collection
    _          = await connect_to_mongo()
    collection =  get_collection(name="products")
    repository = ProductsRepository(collection= collection)
    # 
    collection =  get_collection(name="observatories")
    repository1 = ObservatoriesRepository(collection= collection)
    service1 = ObservatoriesService(repository= repository1)
    # 
    collection =  get_collection(name="catalogs")
    repository2 = CatalogsRepository(collection= collection)
    service2 = CatalogsService(repository= repository2)
    # 
    service = ProductsService(
        repository= repository,
        catalog_service=service2,
        observatory_service=service1
    )
    return repository, service


@pytest.mark.asyncio
async def test_repository_create(products_service):
    repository, _ =  products_service

    # Create a new observatory
    obs = Product(
        pid="myproduct1",
        description="repositoryproduct",
        level_path="",
        product_name="",
        product_type="",
        levels=[
            Level(
                cid="apicatalogcid",
                index=0,
                kind=CatalogKind.INTEREST,
                value="A"
            )
        ], 
        profile="",
        url=""
    )
    res = await repository.create(product=obs)
    print(res)
    assert res.is_ok, "Product creation failed"

@pytest.mark.asyncio
async def test_service_create(products_service):
    _, service =  products_service

    # Create a new observatory
    obs = ProductDTO(
        pid="myproduct1service",
        description="service",
        level_index=0,
        level_path="",
        product_name="",
        product_type="",
        levels=[
            LevelDTO(
                cid="apicatalogcid",
                index=0,
                kind=CatalogKind.INTEREST,
                value="A"
            ),
             LevelDTO(
                cid="apicatalogcid",
                index=1,
                kind=CatalogKind.INTEREST,
                value="B"
            ),  
        ], 
        profile="",
        url=""
    )
    res = await service.create(product=obs)
    print(res)
    assert res.is_ok, "Product creation failed"

@pytest.mark.asyncio
async def test_api_create(products_service):

    # Create a new observatory
    obs = ProductDTO(
        pid="myproduct1api",
        description="repositoryproduct",
        level_path="",
        product_name="",
        product_type="",
        levels=[
            LevelDTO(
                cid="apicatalogcid",
                index=0,
                kind=CatalogKind.INTEREST,
                value="A"
            ),
             LevelDTO(
                cid="apicatalogcid",
                index=1,
                kind=CatalogKind.INTEREST,
                value="B"
            ),  
        ], 
        profile="",
        url=""
    )
    # res = await service.create(product=obs)
    # print(res)
    data = [
        obs.model_dump(mode="json")
    ]
    print(data)
    res = R.post("http://localhost:5000/products", json=data)
    print(res)
    assert res.ok, "Product creation failed"



@pytest.mark.asyncio
async def test_get_products(products_service):
    _, service =  products_service

    res = R.get("http://localhost:5000/products")
    print(res,res.ok)
    assert res.ok,"Fail to get products"

@pytest.mark.asyncio
async def test_filter_products(products_service):
    _, service =  products_service

    obid = "apicreationobs"
    json = {
        # "temporal":{}, 
        # "spatial":{}, 
        "interest":[],
        "tags":["x"]
    }
    res = R.post(f"http://localhost:5000/f/products/{obid}",json=json)
    print(res.json())
    assert res.ok,"Fail to get products"
