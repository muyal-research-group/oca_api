import yaml
from ocaapi.models.v3 import MetaCatalog,Catalog,MetaCatalogCatalog,XVariable,CatalogXVariable,CatalogRelationship,XVariableParent,XTypeEnum,VariableTypeEnum
from pydantic import BaseModel
from typing import List,Any

class XVariablePolicyModel(BaseModel):
    xvid:str
    value: Any
    variable_type:VariableTypeEnum
    parents:List[str]

class CatalogPolicyModel(BaseModel):
    id:str
    name:str
    xtype:XTypeEnum
    xvariables:List[XVariablePolicyModel]
    parents:List[str]

class MetaCatalogPolicyModel(BaseModel):
   id:str
   name:str
   description:str
   catalogs:List[CatalogPolicyModel]

class PolicyModel(BaseModel):
    meta_catalogs: List[MetaCatalogPolicyModel]


class PolicyManager:
    @staticmethod
    def load_from_yaml(path: str) -> dict:
        with open(path, "r") as file:
            return yaml.safe_load(file)

    @staticmethod
    def parse_policy(data: dict) -> PolicyModel:
        meta_catalogs = []
        for mc in data.get("meta_catalogs", []):
            catalogs = []
            for cat in mc.get("catalogs", []):
                xvars = [
                    XVariablePolicyModel(
                        xvid=xv["xvid"],
                        value=xv["value"],
                        variable_type=xv["variable_type"]
                    ) for xv in cat.get("xvariables", [])
                ]
                catalogs.append(CatalogPolicyModel(
                    id=cat["id"],
                    name=cat["name"],
                    xtype=cat["xtype"],
                    xvariables=xvars
                ))
            meta_catalogs.append(MetaCatalogPolicyModel(
                id=mc["id"],
                name=mc["name"],
                description=mc.get("description", ""),
                catalogs=catalogs
            ))
        return PolicyModel(meta_catalogs=meta_catalogs)
