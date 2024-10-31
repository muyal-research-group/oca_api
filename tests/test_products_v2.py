import pytest
from ocaapi.repositories.v2 import ProductRepository,XVariablesRepository,XVariableAssignmentRepository
from ocaapi.dto.v2 import ProductDTO,ProductCreationDTO,ContentVarsDTO,ContextualVariablesDTO,PlotDescriptionDTO
# from ocaapi.dto.v2 import * as DTO
from ocaapi.services.v2 import ProductsService
from ocaapi.models.v2 import ProductModel
from ocaapi.db import get_collection,connect_to_mongo
import requests as R

@pytest.fixture
async def products_service():
    """Fixture to setup the Observatories service and repository."""
    # Setup: Connect to MongoDB and get the collection
    _                    = await connect_to_mongo()
    c                    = get_collection(name="productsv2")
    repository           = ProductRepository(collection=c)
    xvar_repo            = XVariablesRepository(collection=get_collection("xvariables"))
    xvar_assignment_repo = XVariableAssignmentRepository(collection=get_collection("xvariable_assignments"))
    service              = ProductsService(
        repo=repository,
        xvar_assignments_repo=xvar_assignment_repo,
        xvar_repo=xvar_repo
    )
    # Return repository and service for use in tests
    return repository, service



@pytest.mark.skip("")
@pytest.mark.asyncio
async def test_repository_create(products_service):
    repository, _ =  products_service
    # Create a new observatory
    obs = ProductModel(
        pid="repositoryproduct",
        name="Test Repository", 
        description="",
        disabled=False,
    )

    res = await repository.create(product=obs)
    print(res)
    assert res.is_ok, "Product creation failed"
@pytest.mark.skip("")
@pytest.mark.asyncio
async def test_repository_find_all(products_service):
    repository, _ =  products_service
    # Create a new observatory
    res = await repository.find_all(query={},skip=0,limit=0)
    print(res)
    assert res.is_ok, "Product creation failed"
@pytest.mark.skip("")
@pytest.mark.asyncio
async def test_repository_find_by_pid(products_service):
    repository, _ =  products_service
    # Create a new observatory
    res = await repository.find_by_pid(pid="serviceproduct")
    print(res)
    assert res.is_ok, "Product creation failed"
@pytest.mark.skip("")
@pytest.mark.asyncio
async def test_service_create(products_service):
    _,service =  products_service
    # Create a new observatory
    obs = ProductDTO(
        pid="serviceproduct",
        name="Test Service", 
        description="",
    )
    res = await service.create(product=obs)
    print(res)
    assert res.is_ok, "Product creation failed"

@pytest.mark.asyncio
async def test_service_createx(products_service):
    _,service =  products_service
    # Create a new observatory
    xs  = [ 
        # Range, Ranges intermedios operadores logicos.
        # Mortality.RawRatio(100k)
        # Releases.Mean(National,Kg)
        # 
        ProductCreationDTO(
            name           = "Product test 1",
            description    = "A product very chidote 1",
            data_source_id = "mortality_datasource_hash",
            data_view_id   = "mortality_dataview_hash",
            content_vars   = ContentVarsDTO(
                interest_var   = "Sex(Male,Famale), Age([2.20)), CIE10->Chapter(2)->Subchapter(C)->Code(16)->SpecificCause(9)",  
                observable_var  = "Mortality.RawRatio(100k), National.Releases[kg] , State.Releases[Kg], Nom[kg]", # Unit
                info = """
                    Mortality.RawRatio(100k).Sex(Male).Average(2.3), 
                    National.Releases.[IARC(2A), CAS(AS)].Mean(12), State.Releases.Kg.Media(2),
                    Nom.Kg.Min(12)
                """
            ),
            ctx_vars       = ContextualVariablesDTO(
                product_type = "LinePlot",
                spatial_var = "Country(Mexico)->State(San Pancho)->City(Valles)",
                temporal_var = "Year(200)"
            ),
            plot_desc      = PlotDescriptionDTO(
                function_id = "axo_plot_map_id",
                hue         = "Chapters",
                title       = "Mapa chidote",
                x_axis      = "Years",
                y_axis      = "RawRatio100k",
                z_axis      = None,
                # params:Dict[str,str]
            )
        ), 
    ]
    
    i =0 
    for x in xs:
        res = await service.createx(product=x)
        print(res)
        if res.is_ok:
            i+=1
    assert i == len(xs), "Product creation failed"