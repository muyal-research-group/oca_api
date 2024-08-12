from typing import List

# class LevelCatalog(BaseModel):
#     level: int
#     catalog_key: str
class LevelCatalogDTO(object):
    def __init__(self,level:int,cid:str):
        self.level = level
        self.cid = cid
class ObservatoryDTO(object):
    def __init__(self,
                 obid:str,
                #  key:str,
                 title:str,
                 image_url:str,
                 description:str,
                 catalogs:List[LevelCatalogDTO],
    ):
        self.obid = obid
        # self.key = key
        self.title = title
        self.image_url = image_url
        self.description = description 
        self.catalogs = catalogs