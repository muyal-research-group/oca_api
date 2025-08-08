import pytest
from ocaapi.repositories.v2 import ProductRepository,XVariablesRepository,XVariableAssignmentRepository
from ocaapi.dto.v2 import ProductDTO,ProductCreationDTO,PlotDescriptionDTO,ContentVarsDTO,ContextualVariablesDTO
from ocaapi.services.v2 import ProductsService,OcaNameService
from ocaapi.models.v2 import ProductModel
from ocaapi.db import get_collection,connect_to_mongo
import  ocaapi.querylang.peg as qlx
# stats,info_element,info,info_query_left, info_query, info_query_right,info_query_value,sv,sv_element,sv_hierarchy,sv_value
import requests as R
import json as J


# Crear una app web uso con API -> Desarrollo de pa
#


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
        xvar_repo             = xvar_repo,
        xvar_parent_relationship_service = None
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
        res = qlx.stats.parseString(x)
        print("RESULT", res)

@pytest.mark.skip("")
@pytest.mark.asyncio
async def test_info_elemnt():
    xs = [
        "RawRatio100k.Sex(Male).Mean(2.12321)",
    ]
    for  x in xs:
        res = qlx.info_element.parseString(x)
        print("INFO_ELEM<ENT_RESULT", res)

@pytest.mark.skip("")
@pytest.mark.asyncio
async def test_info_query():
    xs = [
        "Info = RawRatio100k.Sex(Male).Mean(2.12321), AIARC-1.Sex(Female).Mean(252.2)",
    ]
    for  x in xs:
        res = qlx.info.parseString(x)
        print("RESUKLT", res)

@pytest.mark.skip("")
@pytest.mark.asyncio
async def test_info_elemnt():
    xs = [
        "RawRatio100k.Sex(Male) < 12",
    ]
    for x in xs:
        res = qlx.info_query_value.parseString(x)
        print(res)

# @pytest.mark.skip("")
@pytest.mark.asyncio
async def test_sv():
    xs = [
        """
        SV = Country(MX),State(Aguas), State(SLP), City(Valles)
        """,
        """
        SV = Country(MX)->State(SLP)
        """,
        """
        SV = Country(MX)->State(SLP)->City(Valles), Country(MX)->State(TAMPS)
        """

    ]
    for x in xs:
        res = qlx.sv.parseString(x)
        print("_"*50)
        print(res)

@pytest.mark.skip("")
@pytest.mark.asyncio
async def test_tv():
    xs = [
        """TV = Date(may,10,1997)""",
        """TV = Date(MaY,10,1997)""",
        """TV = Date(MAY,10,1997)""",
        """TV = *""",
        """TV = [Date(MAY,10,1997), Date(May,10,2024))""",
        """TV = [Date(1,1,1997), Date(1,1,2024))""",
        """TV = [Date(1,1,1997), Date(1,1,2024))""",
        """TV = [Date(1,1,1997), Date(1,1,2024))""",
    ]
    for x in xs:
        res = qlx.tv.parseString(x)
        print(res)

@pytest.mark.skip("")
@pytest.mark.asyncio
async def test_iv_ranges():
    xs = [
        """Age([1.2,2])""",
        """Age((1,2])""",
        """Age([1.1,100])""",
    ]
    for x in xs:
        res = qlx.iv_ranges.parseString(x)
        print(res)

@pytest.mark.skip("")
@pytest.mark.asyncio
async def test_iv():
    xs = [
        "IV = Sex(Male,Female)",
        "IV = Chapter(2)->Subchapter(C)->Code(16)->SpecificCause(9)",
        # """IV = Sex(Male,Female), Age([1,85)), Chapter(2)->Subchapter(C)->Code(16)->SpecificCause(9)""",
    ]

    for x in xs:
        print("_"*20)
        res = qlx.iv.parseString(x)
        print(res)
        print("_"*20)

@pytest.mark.skip("")
@pytest.mark.asyncio
async def test_ov():
    xs = [
        """OV = Mortality.RawRatio(100k)""",
        """OV = Mortality.RawRatio()""",
        """OV = Mortality.RawRatio(1k), Mortality.RawRatio(10k), Mortality.RawRatio(100k)""",
        """OV = National.Releases(kg)""",
    ]
    for x in xs:
        print("_"*20)
        res = qlx.ov.parseString(x)
        print(res)

@pytest.mark.skip("")
@pytest.mark.asyncio
async def test_info():
    xs = [
        """Info = Mortality.RawRatio(100k).Sex(Male).Average(20)""",
        """Info = Mortality.RawRatio(100k).[Sex(Male,Female), Color(Red)].Average(20), Mortality.RawRatio(100k).[Sex(Male,Female), Color(Red)].Median(20)""",
        """Info = Mortality.Counting().CauseOfDeath(A,C,E,B,D).MEAN(51006.2), Mortality.Counting().CauseOfDeath(A,C,E,B,D).MEDIAN(13372.0), Mortality.Counting().CauseOfDeath(A,C,E,B,D).MIN(6521.0), Mortality.Counting().CauseOfDeath(A,C,E,B,D).MAX(132468.0), Mortality.Counting().CauseOfDeath(A,C,E,B,D).STD(56857.09796674466)"""
    ]
    for x in xs:
        print("_"*20)
        res = qlx.info.parseString(x)
        print(res)
        print("_"*20)

@pytest.mark.skip("")
@pytest.mark.asyncio
async def test_pt():
    xs = [
        """ProductType = Map"""
    ]
    for x in xs:
        print("_"*20)
        res = qlx.pt.parseString(x)
        print(res)
        print("_"*20)

@pytest.mark.skip("")
@pytest.mark.asyncio
async def test_oca():
    xs = [
        """
            SV = Country(MX) -> State(SLP) -> Municipilaty(Ciudad Valles)
            TV = [Date(5, 10, 1996), Date(1,1,2024)]
            IV = Sex(Male,Female)
            OV = Mortality.RawRatio(100k)
            Info = Mortality.RawRatio(100k).Sex(Male).Average(10)
            ProductType = Map
        """,
        """
            SV = Country(MX) -> State(SLP) -> Municipilaty(Ciudad Valles)
            TV = *
            IV = *
            OV = *
            Info = *
            ProductType = *
        """
    ]
    for x in xs:
        print("_"*20)
        res = qlx.grammar.parseString(x)
        print("_"*20)
