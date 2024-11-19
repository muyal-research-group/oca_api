import pytest
from ocaapi.repositories.v2 import ProductRepository,XVariablesRepository,XVariableAssignmentRepository,XVariableParentRelationshipRepository
from ocaapi.dto.v2 import ProductDTO
from ocaapi.querylang.dto import ProductCreationDTO,ContentVarsDTO,ContextualVariablesDTO,PlotDescriptionDTO
from ocaapi.services.v2 import ProductsService,XVariableParentRelationshipService,XVariablesService
from ocaapi.models.v2 import ProductModel
from ocaapi.db import get_collection,connect_to_mongo
import requests as R

@pytest.fixture
async def products_service():
    """Fixture to setup the service and repository."""
    # Setup: Connect to MongoDB and get the collection
    _                                = await connect_to_mongo()
    c                                = get_collection(name="productsv2")
    cc                               = get_collection(name="xvariable_parent_relatioship")
    repository                       = ProductRepository(collection=c)
    xvar_repo                        = XVariablesRepository(collection=get_collection("xvariables"))
    xvar_service                     = XVariablesService(repo = xvar_repo)
    xvar_assignment_repo             = XVariableAssignmentRepository(collection=get_collection("xvariable_assignments"))
    xvar_parent_relationship_repo    = XVariableParentRelationshipRepository(collection=cc)
    xvar_parent_relationship_service = XVariableParentRelationshipService(repo = xvar_parent_relationship_repo)
    service                          = ProductsService(
        repo                             = repository,
        xvar_assignments_repo            = xvar_assignment_repo,
        xvar_repo                        = xvar_repo,
        xvar_service                     = xvar_service,
        xvar_parent_relationship_service = xvar_parent_relationship_service
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

@pytest.mark.skip("")
@pytest.mark.asyncio
async def test_product_creation_from_json(products_service):
    _,service =  products_service
    paths = [
        "/home/nacho/Programming/Python/oca_api/data/example/bf62c0a74a2705f78a23a6313b3f9f98bf7cd85926cced502c7967a98f1f316d_metadata.json",
        "/home/nacho/Programming/Python/oca_api/data/a.json",
        # "/home/nacho/Programming/Python/oca_api/data/b.json",

    ]
    for path in paths:
        p = ProductCreationDTO.from_json_file(path = path)
        print(p)
        print(p.parse())

@pytest.mark.skip("")
@pytest.mark.asyncio
async def test_product_creation(products_service):

    
    _,service =  products_service
    ps = [
        ProductCreationDTO(
            name           = "My product",
            data_source_id = "DATA_SOURCE_ID",
            data_view_id   = "DATA_VIEW_ID",
            description    = "A simple description",
            plot_desc      = PlotDescriptionDTO(
                function_id = "FUNCTION_ID",
                hue         = "",
                title       = "The plot",
                x_axis      = "X_AXIS",
                y_axis      = "Y_AXIS",
                z_axis      = "Z_AXIS"
            ),
            ctx_vars       = ContextualVariablesDTO(
                spatial_var  = "Country(MX)->State(SLP)->City(Valles)",
                temporal_var = "Date(0,0,2020)",
                product_type = "Map"
            ),
            content_vars   = ContentVarsDTO(
                interest_var   = "Sex(Male,Female), Color(RED)",
                observable_var = "Mortality.RawRatio(100k)",
                info           = "Mortality.RawRatio(100k).[Sex(Male,Female),Color(RED)].Average(20.5)"
            )
        ),
        ProductCreationDTO(
            name           = "My product 2",
            data_source_id = "DATA_SOURCE_ID",
            data_view_id   = "DATA_VIEW_ID",
            description    = "A simple description",
            plot_desc      = PlotDescriptionDTO(
                function_id = "FUNCTION_ID",
                hue         = "",
                title       = "The plot",
                x_axis      = "X_AXIS",
                y_axis      = "Y_AXIS",
                z_axis      = "Z_AXIS"
            ),
            ctx_vars       = ContextualVariablesDTO(
                spatial_var  = "Country(MX)",
                temporal_var = "[Date(1,1,2020), Date(1,1,2024)]",
                product_type = "Map"
            ),
            content_vars   = ContentVarsDTO(
                interest_var   = "Sex(Male,Female), Color(RED)",
                observable_var = "Mortality.RawRatio(100k)",
                info           = "Mortality.RawRatio(100k).[Sex(Male),Color(RED)].Average(20.5)"
            )
        )
    ]
    for x in ps:
        
        res = await service.create(product=x)
        print("_"*30)
        # parsed = x.parse()
        # print(parsed.get("sv"))