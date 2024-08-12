from typing import Dict,Union,List
class CatalogItemDTO(object):

    def __init__(self,
                 value:str,
                 display_name:str,
                 code:int,
                 description:str,
                 metadata:Dict[str,str]={}
    ):
        # self.key         
        self.value         = value
        self.display_name = display_name
        self.code         = code
        self.description  = description
        self.metadata     = metadata
    
class CatalogDTO(object):
    def __init__(self,
                 display_name:str,
                 items:List[CatalogItemDTO],cid:str="",
                 kind:str="",
                 ):
        self.cid          = cid
        # self.name         = name
        self.display_name = display_name
        self.items        = items
        self.kind = kind