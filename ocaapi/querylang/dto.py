from typing import Optional,Dict, Any
import ocaapi.querylang.peg as qlx
from pydantic import BaseModel
import json as J 
class PlotDescriptionDTO(BaseModel):
    function_id: Optional[str] = ""
    x_axis     :Optional[str]  = ""
    y_axis     :Optional[str]  = ""
    z_axis     :Optional[str]  = ""
    hue        :Optional[str]  = ""
    title:Optional[str] =""
    params: Optional[Dict[str, Any]] = {}

class ContextualVariablesDTO(BaseModel):
    spatial_var: Optional[str] = ""
    temporal_var: Optional[str] = ""
    product_type: Optional[str] = ""

class ContentVarsDTO(BaseModel):
    interest_var   :Optional[str] = ""
    observable_var :Optional[str] = ""
    info           :Optional[str] = ""

class ProductCreationDTO(BaseModel):
    name          : str
    description   : Optional[str] = ""
    data_source_id: Optional[str] = ""
    data_view_id  : Optional[str] = ""
    plot_desc     : PlotDescriptionDTO
    ctx_vars      : ContextualVariablesDTO
    content_vars  : ContentVarsDTO
    def parse(self):
        x = f"""
            SV          = {self.ctx_vars.spatial_var}
            TV          = {self.ctx_vars.temporal_var}
            IV          = {self.content_vars.interest_var}
            OV          = {self.content_vars.observable_var}
            Info        = {self.content_vars.info}
            ProductType = {self.ctx_vars.product_type}
        """
        return qlx.grammar.parseString(x).asDict()
    @staticmethod
    def from_json_file(path:str)->"ProductCreationDTO":
        with open(path,"rb") as f:
            metadata = J.load(f)
            return ProductCreationDTO(
                **metadata
            )
            # print("METADATA",metadata)
                
        # print("SV",sv)
        # print("PARSE", parsed)