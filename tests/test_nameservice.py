import pytest
from ocaapi.repositories.v2 import ProductRepository,XVariablesRepository,XVariableAssignmentRepository
from ocaapi.dto.v2 import ProductDTO,ProductCreationDTO
from ocaapi.services.v2 import ProductsService,OcaNameService
from ocaapi.models.v2 import ProductModel
from ocaapi.db import get_collection,connect_to_mongo
from ocaapi.querylang.peg import stats,info_element,info,info_query_left, info_query, info_query_right,info_query_value
import requests as R

@pytest.fixture
async def get_nameservice():
    # Setup: Connect to MongoDB and get the collection
    _                          = await connect_to_mongo()
    c                          = get_collection(name="productsv2")
    product_repository                 = ProductRepository(collection=c)
    xvar_repo                  = XVariablesRepository(collection=get_collection("xvariables"))
    xvariable_assignments_repo = XVariableAssignmentRepository(collection=get_collection("xvariable_assignments"))
    product_service            = ProductsService(
        repo                  = product_repository,
        xvar_assignments_repo = xvariable_assignments_repo,
        xvar_repo             = xvar_repo
    )
    oca_nameservice = OcaNameService(
        xvariable_assignments_repo = xvariable_assignments_repo,
        product_repo= product_repository
    )
    
    return None, oca_nameservice


@pytest.mark.skip("")
@pytest.mark.asyncio
async def test_repository_filter(get_nameservice):
    _, service = get_nameservice
    # SV          = Country(Mexico)->State(San Luis Potosi)
    query = """
    SV          = Country(Mexico)->State(San Luis Potosi)
    TV          = Year(2000)
    IV          = Sex(Female,Male), Substance(BI) 
    VO          = RawRatio100k
    Info        = RawRatio100k.Sex(Male) == Median[RawRatio100k.Sex(Male)]
    ProductType = Barplot 
    """
    res = await service.filter(query)
    print("RES",res)
    assert True, "Failed filtering"


@pytest.mark.skip("")
@pytest.mark.asyncio
async def test_stats():
    xs = [
        "Mean(2)",
        "Average(2.3)",
        "Median(3.123123)",
        "STD(2.34)",
        "Q1(2.4)",
        "Q2(32.4)",
        "Q3(345.54335)",
        "Variance(2.43434)"
    ]
    for  x in xs:
        res = stats.parseString(x)
        print("RESULT", res)

@pytest.mark.skip("")
@pytest.mark.asyncio
async def test_info_elemnt():
    xs = [
        "RawRatio100k.Sex(Male).Mean(2.12321)",
    ]
    for  x in xs:
        res = info_element.parseString(x)
        print("INFO_ELEM<ENT_RESULT", res)
@pytest.mark.skip("")
@pytest.mark.asyncio
async def test_info_query():
    xs = [
        "Info = RawRatio100k.Sex(Male).Mean(2.12321), AIARC-1.Sex(Female).Mean(252.2)",
    ]
    for  x in xs:
        res = info.parseString(x)
        print("RESUKLT", res)

@pytest.mark.asyncio
async def test_info_elemnt():
    xs = [
        "RawRatio100k.Sex(Male) < 12",
    ]
    for x in xs:
        res = info_query_value.parseString(x)
        print(res)