class ProductDTO(object):
    def __init__(self,description:str, product_type:str, kind: str, level_index:int, level_path:str, profile:str, product_name:str):
        self.description     = description
        self.product_type    = product_type 
        self.kind            = kind
        self.level_index:int = level_index
        self.level_path:str  = level_path
        self.profile:str     = profile
        self.product_name    = product_name