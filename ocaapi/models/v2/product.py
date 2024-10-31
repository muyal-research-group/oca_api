from pydantic import BaseModel, Field
from typing import Optional
class PlotDescription(BaseModel):
    function_id :Optional[str] = ""
    x_axis      :Optional[str] = ""
    y_axis      :Optional[str] = ""
    z_axis      :Optional[str] = ""
    hue         :Optional[str] = ""
    title       :Optional[str] = ""
class ContextualVariables(BaseModel):
    spatial_var: Optional[str] = ""
    temporal_var: Optional[str] = ""
    product_type: Optional[str] = ""

class ContentVars(BaseModel):
    interest_var   :Optional[str] = ""
    observable_var :Optional[str] = ""
    info           :Optional[str] = ""

class ProductModel(BaseModel):
    pid           : str
    name          : str
    description   : Optional[str] = ""
    data_source_id: Optional[str] =""
    data_view_id  : Optional[str] = ""
    plot_desc     : PlotDescription
    ctx_vars      : ContextualVariables
    content_vars  : ContentVars
    disabled      : Optional[bool]= False
