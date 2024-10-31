import pytest
from ocaapi.repositories.v2 import XVariablesRepository,XVariableAssignmentRepository
from ocaapi.dto.v2 import XVariableDTO,MultipleXVariableAssignmentDTO,ManyProductsMultipleXVariableAssignmentDTO,XVariableRawAssignmentDTO
from ocaapi.services.v2 import XVariablesService,XVariableAssignmentsService
from ocaapi.models.v2 import XVariableModel,XVariableAssignment
from ocaapi.db import get_collection,connect_to_mongo
import requests as R
import json as J

@pytest.fixture
async def xvariables_service():
    """Fixture to setup the Observatories service and repository."""
    # Setup: Connect to MongoDB and get the collection
    _          = await connect_to_mongo()
    c          = get_collection(name="xvariables")
    repository = XVariablesRepository(collection=c)
    xvrepo     = XVariableAssignmentRepository(collection= get_collection("xvariablesassignments"))
    xservice   = XVariableAssignmentsService(repo= xvrepo)
    service    = XVariablesService(repo=repository)
    # Return repository and service for use in tests
    return repository, service,xservice

@pytest.mark.skip("")
@pytest.mark.asyncio
async def test_repository_create(xvariables_service):
    repository, _,_ =  xvariables_service

    # Create a new observatory
    obs = XVariableModel(
        type="AgeRange",
        value="00-04",
        xvid=""
    )
    res = await repository.create(variable=obs)
    assert res.is_ok, "Observatory creation failed"

@pytest.mark.skip("")
@pytest.mark.asyncio
async def test_service_create(xvariables_service):
    _, service,_ =  xvariables_service

    # Create a new observatory
    obs = XVariableDTO(
        xvid="agerange0044",
        type="AgeRange",
        value="00-04",
        parent_id=None
    )
    res = await service.create(xvariable=obs)
    assert res.is_ok, "Observatory creation failed"


@pytest.mark.skip("")
@pytest.mark.asyncio
async def test_repo_find_by_xvid(xvariables_service):
    repo, _,_ =  xvariables_service
    res = await repo.find_by_xvid(xvid="fc41e42be537cc344b24f528dd65a521cac753d2aac29e6886d5e282237de2e7")
    print(res)
    assert res.is_ok, "Failed to find by xvid"

@pytest.mark.skip("")
@pytest.mark.asyncio
async def test_repo_find_by_type_value(xvariables_service):
    repo, _,_ =  xvariables_service
    res = await repo.find_by_type_value(
        type="AgeRange",
        value="00-04"
    )

    print(res)
    assert res.is_ok, "Failed to find by type and value"

@pytest.mark.skip("")
@pytest.mark.asyncio
async def test_service_find_by_xvid(xvariables_service):
    _, service,_ =  xvariables_service
    res = await service.find_by_xvid(xvid="fc41e42be537cc344b24f528dd65a521cac753d2aac29e6886d5e282237de2e7")
    print(res)
    assert res.is_ok, "Failed to find by xvid"

@pytest.mark.skip("")
@pytest.mark.asyncio
async def test_api_create(xvariables_service):
    _, service,_ =  xvariables_service

    # Create a new observatory
    with open("/home/nacho/Programming/Python/oca_api/data/age_range_v2.json","rb") as f:
        data = J.load(f)
        print(data)
        kind = data["type"]
        json =[]
        for value in data["values"]:
            json.append(
                XVariableDTO(
                    type=kind,
                    value=value["value"],
                    description=value["description"]
                ).model_dump()
            )
    
  
    res = R.post("http://localhost:5000/v2/xvariables",json=json )
    print(res)
    # res = await service.create(xvariable=obs)
    assert res.ok, "Observatory creation failed"

@pytest.mark.skip("")
@pytest.mark.asyncio
async def test_api_assign(xvariables_service):
    _, service,_ =  xvariables_service

    json = MultipleXVariableAssignmentDTO(
        xid="",
        assignments=[
            XVariableRawAssignmentDTO(kind="",value="")
        ]
    )
    res = R.post("http://localhost:5000/v2/xvariables/assign",json=json )
    print(res)
    # res = await service.create(xvariable=obs)
    assert res.ok, "Observatory creation failed"




# @pytest.mark.asyncio
# async def test_xvariable_assign(xvariables_service):
#     _, _,xservice =  xvariables_service

#     # Create a new observatory
#     res = await xservice.create(
#         productxvariable=XVariableAssignment(
#             xoid="myproduct1api",
#             xvid="agerange0044"
#         )
#     )
#     print(res)
#     assert res.is_ok, "Relation Product XVariable creation failed"
