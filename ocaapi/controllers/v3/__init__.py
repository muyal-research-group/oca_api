from fastapi import APIRouter, Depends
from ocaapi.models.v3 import MetaCatalog,Catalog,XVariable,MetaCatalogCatalog,XVariableParent,CatalogRelationship,CatalogXVariable
from ocaapi.services.v3 import MetaCatalogService,CatalogService,XVariableService,MetaCatalogCatalogService,CatalogXVariableService,XVariableParentService,CatalogRelationshipService
from ocaapi.repositories.v3 import MetaCatalogRepository,CatalogRepository,XVariableRepository,MetaCatalogCatalogRepository,CatalogXVariableRepository,XVariableParentRepository,CatalogRelationshipRepository
from ocaapi.policy import PolicyModel
from ocaapi.db import get_collection 

def get_metadata_catalog_catalog_service()->MetaCatalogCatalogService:
    collection =  get_collection(name="meta_catalog_catalog")
    repository = MetaCatalogCatalogRepository(collection= collection)
    service = MetaCatalogCatalogService(repository= repository)
    return service

def get_metadata_catalog_service()->MetaCatalogService:
    collection =  get_collection(name="meta_catalog")
    repository = MetaCatalogRepository(collection= collection)
    service = MetaCatalogService(repository= repository)
    return service

def get_catalog_service()->CatalogService:
    collection =  get_collection(name="catalog")
    repository = CatalogRepository(collection= collection)
    service = CatalogService(repository= repository)
    return service

def get_xvar_service()->XVariableService:
    collection =  get_collection(name="xvars")
    repository = XVariableRepository(collection= collection)
    service = XVariableService(repository= repository)
    return service

def get_catalog_xvar_service()->CatalogXVariableService:
    collection =  get_collection(name="catalog_xvar")
    repository = CatalogXVariableRepository(collection= collection)
    service = CatalogXVariableService(repository= repository)
    return service
def get_catalog_relatioshiop_service()->CatalogRelationshipService:
    collection =  get_collection(name="catalog_relatioship")
    repository = CatalogRelationshipRepository(collection= collection)
    service = CatalogRelationshipService(repository= repository)
    return service
def get_xvar_parent_service()->XVariableParentService:
    collection =  get_collection(name="xvar_parent")
    repository = XVariableParentRepository(collection= collection)
    service = XVariableParentService(repository= repository)
    return service
router = APIRouter()



# Dependency Injection Example (would be better modularized per entity)
@router.post("/metacatalogs/policy")
async def index_by_policy(
    policy:PolicyModel,
    meta_catalog_service: MetaCatalogService = Depends(get_metadata_catalog_service), 
    catalog_service:CatalogService = Depends(get_catalog_service),
    xvar_service:XVariableService = Depends(get_xvar_service),
    meta_catalog_catalog_service:MetaCatalogCatalogService = Depends(get_metadata_catalog_catalog_service),
    catalog_xvar_service:CatalogXVariableService = Depends(get_catalog_xvar_service),
    catalog_rel_service: CatalogRelationshipService = Depends(get_catalog_relatioshiop_service),
    xvar_parent_service: XVariableParentService = Depends(get_xvar_parent_service)
):
    print(policy)
    catalog_ids = {}
    xvar_ids = {}

    for mc in policy.meta_catalogs:
        mc_id = await meta_catalog_service.create(MetaCatalog(mcid=mc.id,name=mc.name, description=mc.description))
        for cat in mc.catalogs:
            catalog = Catalog(cid= cat.id, name=cat.name, xtype=cat.xtype.value, description="")
            cat_id = await catalog_service.create(catalog)
            catalog_ids[cat.id] = cat_id
            await meta_catalog_catalog_service.create(MetaCatalogCatalog(meta_catalog_id=mc_id, catalog_id=cat_id))

            for xv in cat.xvariables:
                xvar_model = XVariable(
                    xvid=xv.xvid,
                    xtype=cat.xtype,
                    value=xv.value,
                    variable_type=xv.variable_type
                )
                xvar_id = await xvar_service.create(xvar_model)
                xvar_ids[xv.xvid] = xvar_id
                await catalog_xvar_service.create(CatalogXVariable(catalog_id=cat_id, xvariable_id=xvar_id))

    for mc in policy.meta_catalogs:
        for cat in mc.catalogs:
            for parent_id in cat.parents or []:
                await catalog_rel_service.create(CatalogRelationship(
                    catalog_id=catalog_ids[cat.id],
                    parent_catalog_id=catalog_ids[parent_id]
                ))
            for xv in cat.xvariables:
                for p in xv.parents:
                    await xvar_parent_service.create(XVariableParent(
                        xvariable_id=xvar_ids[xv.xvid],
                        parent_xvariable_id=xvar_ids[p]
                    ))
    return "Ok"

@router.post("/metacatalogs")
async def create_metacatalog(mc: MetaCatalog, service: MetaCatalogService = Depends(get_metadata_catalog_service)):
    return await service.create(mc)

@router.get("/metacatalogs")
async def list_metacatalogs(service: MetaCatalogService = Depends(get_metadata_catalog_service)):
    return await service.get_all()

@router.post("/catalogs")
async def create_catalog(c: Catalog, service: CatalogService = Depends(get_catalog_service)):
    return await service.create(c)

@router.get("/catalogs")
async def list_catalogs(service: CatalogService = Depends(get_catalog_service)):
    return await service.get_all()

@router.post("/xvariables")
async def create_xvar(xv: XVariable, service: XVariableService = Depends(get_xvar_service)):
    return await service.create(xv)

@router.get("/xvariables")
async def list_xvars(service: XVariableService = Depends(get_xvar_service)):
    return await service.get_all()
