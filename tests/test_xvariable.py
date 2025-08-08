import pytest
from typing import List
from ocaapi.repositories.v2 import XVariablesRepository,XVariableAssignmentRepository,XVariableParentRelationshipRepository
from ocaapi.dto.v2 import XVariableDTO,MultipleXVariableAssignmentDTO,ManyProductsMultipleXVariableAssignmentDTO,XVariableRawAssignmentDTO
from ocaapi.services.v2 import XVariablesService,XVariableAssignmentsService,XVariableParentRelationshipService
from ocaapi.models.v2 import XVariableModel,XVariableAssignment,XVariableType,XType
from ocaapi.db import get_collection,connect_to_mongo
import requests as R
import json as J
import datetime

@pytest.fixture
async def xvariables_service():
    """Fixture to setup services and repositories."""
    # Setup: Connect to MongoDB and get the collection
    _          = await connect_to_mongo()
    c          = get_collection(name="xvariables")
    repository = XVariablesRepository(collection=c)
    xvrepo     = XVariableAssignmentRepository(collection= get_collection("xvariablesassignments"))
    xservice   = XVariableAssignmentsService(repo= xvrepo)
    xvrs       = XVariableParentRelationshipRepository(collection=get_collection("xvariable_parent_relatioship"))
    parent_rs  = XVariableParentRelationshipService(repo =xvrs)
    service    = XVariablesService(repo=repository,parent_relationship=parent_rs)
    # Return repository and service for use in tests
    return repository, service,xservice




# @pytest.skip("")
@pytest.mark.asyncio
async def test_service_create_ids(xvariables_service):
    _, service,_ =  xvariables_service

    xs:List[XVariableDTO] =[
        XVariableDTO(
            type          = "Chapter",
            value         = "II",
            xtype=XType.String,
            description   = "A chapter",
            variable_type = XVariableType.Interest,
            xvid          = "",
            raw           = "Chapter(II)",
            order         = 1
        ),
        XVariableDTO(
            type          = "Block",
            value         = "C50",
            xtype=XType.String,
            description   = "A block",
            variable_type = XVariableType.Interest,
            xvid          = "",
            raw           = "Block(C50)",
            order         = 2
        ),
        XVariableDTO(
            type          = "Sex",
            value         = ["Male","Female"],
            xtype         = XType.Array,
            description   = "sexes",
            variable_type = XVariableType.Interest,
            raw           = "Sex([Male, Female])",
            order         = -1
        ),
        XVariableDTO(
            type          = "Date",
            value         = datetime.datetime(2024,1,1),
            xtype=XType.Date,
            description   = "A date",
            variable_type = XVariableType.Temporal,
            xvid          = "",
            raw           = "Date(1,1,2024)",
            order         = -1
        ),
        XVariableDTO(
            type  = "DateRange",
            value = {
                "start"     : datetime.datetime(2000,1,1),
                "end"       : datetime.datetime(2024,1,1),
                "left_open" : False,
                "right_open": False
            },
            xtype         = XType.DateRange,
            description   = "A date range",
            variable_type = XVariableType.Temporal,
            xvid          = "",
            raw           = "",
            order         = -1
        ),
        XVariableDTO(
            type  = "Range",
            value = {
                "start"     : 0,
                "end"       : 10,
                "step"      : 1,
                "left_open" : False,
                "right_open": False
            },
            xtype         = XType.Range,
            description   = "A range",
            variable_type = XVariableType.Interest,
            xvid          = "",
            raw           = "",
            order         = -1
        ),
        XVariableDTO(
            xvid        = "",
            description = "",
            raw         = "AgeRange(0-4)", # 0-4
            order         = 1,
            type          = "AgeRange",
            value         = "0-4",
            variable_type = XVariableType.Interest,
            xtype         = XType.String
        ),
        XVariableDTO(
            xvid          = "",
            description   = "",
            raw           = "AgeRange(5-9)",        # 0-4
            order         = 2,
            type          = "AgeRange",
            value         = "5-9",
            variable_type = XVariableType.Interest,
            xtype         = XType.String
        ),
         XVariableDTO(
            xvid        = "",
            description = "",
            raw         = "Chapter(I)", # 0-4
            order         = 1,
            type          = "Chapter",
            value         = "I",
            variable_type = XVariableType.Interest,
            xtype         = XType.String,
        ),
         XVariableDTO(
            xvid          = "",
            description   = "",
            raw           = "Category(A)",          # 0-4
            order         = 2,
            type          = "Category",
            value         = "A",
            variable_type = XVariableType.Interest,
            xtype         = XType.String,
        ),
        XVariableDTO(
            xvid          = "",
            description   = "",
            raw           = "Group(00)",              # 0-4
            order         = 3,
            type          = "Group",
            value         = "A",
            variable_type = XVariableType.Interest,
            xtype         = XType.String,
        ),

        
        # CHAPTER.CATEGORY.GROUP.SUBCATEGORY? 
    
    ] 
    
    
    for x in xs:
        x.build()
        print(x)
        print("_"*50)
    res = await service.create_many(xs = xs)
    assert True,"Failed to calculate ids"

@pytest.mark.skip("")
@pytest.mark.asyncio
async def test_service_create_ordered(xvariables_service):
    _, service,_ =  xvariables_service
    xs = [
        XVariableDTO(
            type          = "Chapter",
            value         = "II",
            xtype=XType.String,
            description   = "A chapter",
            variable_type = XVariableType.Interest,
            xvid          = "",
            raw           = "Chapter(II)",
            order         = 1
        ),
        XVariableDTO(
            type          = "Block",
            value         = "C50",
            description   = "A block",
            variable_type = XVariableType.Interest,
            xtype=XType.String,
            xvid          = "",
            raw           = "C50",
            order         = 2
        ),
        XVariableDTO(
            type          = "Modifier",
            value         = "4",
            description   = "A modifer",
            variable_type = XVariableType.Interest,
            xtype=XType.String,
            xvid          = "",
            raw           = "4",
            order         = 3
        )
    ]

    # for o in xs:
    res = await service.create_ordered(xs=xs)
    print("RE",res)
    assert True, "XVariable creation failed"


@pytest.mark.skip("")
@pytest.mark.asyncio
async def test_service_create(xvariables_service):
    _, service,_ =  xvariables_service

    obs = [
        XVariableDTO(
            type          = "DateRange",
            value         = {
                "start": datetime.datetime(2020,10,6), 
                "end":datetime.datetime(2000,10,6), 
                "inclusive":True
            },
            description   = "A date rage",
            variable_type = XVariableType.Temporal,
            xvid          = "",
            raw="[Date(10,6,2000), Date(10,6,2020)]"
        ),
        XVariableDTO(
            type          = "Date",
            value         = datetime.datetime(2000,1,1),
            description   = "A date",
            variable_type = XVariableType.Temporal,
            xvid          = "",
            raw = "Date(1,1,2000)"
        ),
        XVariableDTO(
            type          = "Chapter(2)",
            value         = "2",
            description   = "A chapter",
            variable_type = XVariableType.Interest,
            xvid          = "",
            raw = "Chapter(1)" 
        ),

        XVariableDTO(
            type          = "PositiveIntRange",
            value         = {
                "start":10,
                "end":89,
                "interval":1,
                "inclusive":True
            },
            description   = "A positive int range",
            variable_type = XVariableType.Interest,
            xvid          = "",
            raw = "Age([10,89,1])"
        ),
        XVariableDTO(
            type          = "Range",
            value         = {
                "start":-10,
                "end":89,
                "interval":2,
                "inclusive":True
            },
            description   = "A  range",
            variable_type = XVariableType.Interest,
            xvid          = "",
            raw = "Range([-10,89,2])"
        ),

        XVariableDTO(
            type          = "Chapter",
            value         = "II",
            xtype=XType.String,
            description   = "A chapter",
            variable_type = XVariableType.Interest,
            xvid          = "",
            raw           = "Chapter(II)",
            order         = 1
        ),
        XVariableDTO(
            type          = "Block",
            value         = "C50",
            description   = "A block",
            variable_type = XVariableType.Interest,
            xtype=XType.String,
            xvid          = "",
            raw           = "C50",
            order         = 2
        )
        
    ]
    for o in obs:
        res = await service.create(xvariable=o)
        print("RE",res)
    assert True, "XVariable creation failed"


@pytest.mark.skip("")
@pytest.mark.asyncio
async def test_repository_create(xvariables_service):
    repository, _,_ =  xvariables_service

    # Create a new observatory
    obs = XVariableModel(
        type="DateRange",
        value=[ datetime.datetime(2020,10,6), datetime.datetime(2000,10,6)],
        description="A date rage",
        variable_type=XVariableType.Temporal,
        xvid=""
    )
    res = await repository.create(variable=obs)
    assert res.is_ok, "Observatory creation failed"

# @pytest.mark.skip("")


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




