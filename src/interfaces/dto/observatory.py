from typing import List

# class LevelCatalog(BaseModel):
#     level: int
#     catalog_key: str
class LevelCatalogDTO(object):
    def __init__(self,level:int,catalog_key:str):
        self.level = level
        self.catalog_key = catalog_key
class ObservatoryDTO(object):
    def __init__(self,
                 key:str,
                 title:str,
                 image_url:str,
                 description:str,
                 catalogs:List[LevelCatalogDTO]
    ):
        self.key = key
        self.title = title
        self.image_url = image_url
        self.description = description 
        self.catalogs = catalogs