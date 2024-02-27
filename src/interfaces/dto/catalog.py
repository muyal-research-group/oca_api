from typing import Dict,Union,List
class CatalogItemDTO(object):

    def __init__(self,
                 name:str,
                 display_name:str,
                 code:str,
                 description:str,
                 metadata:Dict[str,str]
    ):
        # self.key         
        self.name         = name
        self.display_name = display_name
        self.code         = code
        self.description  = description
        self.metadata     = metadata
    
class CatalogDTO(object):
    def __init__(self,name:str,display_name:str,items:List[CatalogItemDTO],key:str=""):
        self.key          = key
        self.name         = name
        self.display_name = display_name
        self.items        = items