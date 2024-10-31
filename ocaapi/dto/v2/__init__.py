from typing import Optional,List,Tuple, Any,Generator
from pydantic import BaseModel
from ocaapi.models.v2 import XVariableModel
import hashlib as H

class ObservatoryDTO(BaseModel):
    obid: str
    title: str
    description: Optional[str]=""
    image: Optional[str]="https://static.vecteezy.com/system/resources/thumbnails/004/141/669/small/no-photo-or-blank-image-icon-loading-images-or-missing-image-mark-image-not-available-or-image-coming-soon-sign-simple-nature-silhouette-in-frame-isolated-illustration-vector.jpg"
class XVariableAssignmentDTO(BaseModel):
    xid:str
    xvid:str
class XVariableDTO(BaseModel):
    xvid: Optional[str] = ""
    type: str
    value: str
    description:Optional[str]="No description yet."
    parent_id: Optional[str] = None
    @staticmethod
    def from_model(x:XVariableModel)->'XVariableDTO':
        return XVariableDTO(
            **x.model_dump()
        )

# class XVariableAssignmentDTO()

class ProductDTO(BaseModel):
    pid: str
    name: str
    description: Optional[str]=""


class TagDTO(BaseModel):
    type: str
    value: str

class ProductFoundDTO(BaseModel):
    pid: str
    name: str
    description: Optional[str]=""
    tags:Optional[List[TagDTO]] = []



class PlotDescriptionDTO(BaseModel):
    function_id: Optional[str] = ""
    x_axis     :Optional[str]  = ""
    y_axis     :Optional[str]  = ""
    z_axis     :Optional[str]  = ""
    hue        :Optional[str]  = ""
    title:Optional[str] =""

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
 
class XVariableRawAssignmentDTO(BaseModel):
    kind: str
    value: str

class MultipleXVariableAssignmentDTO(BaseModel):
    xid: str
    is_product: Optional[bool] = False
    assignments: Optional[List[XVariableRawAssignmentDTO]]=[]

class ManyProductsMultipleXVariableAssignmentDTO(BaseModel):
    xid: Optional[List[str]] = []
    is_product: Optional[bool] = False
    assignments: Optional[List[XVariableRawAssignmentDTO]]=[]



class XVariableInfoDTO(BaseModel):
    type: str
    value: str
    # def fr
    def calculate_hash(self):
        h = H.sha256()
        h.update(f"{self.type}{self.value}".encode())
        return h.hexdigest()

class XVariableMultipleInfoWithXVId(BaseModel):
    xvid: Optional[str]=""
    types: Optional[List[str]]=[]
    values: Optional[List[str]] = []
    # def fr
    def calculate_hash(self):
        h = H.sha256()
        for t,v in zip(self.types,self.values):
            h.update(f"{t}{v}".encode())
        return h.hexdigest()
    def to_tags(self):
        for t,v in zip(self.types, self.values):
            yield TagDTO(type = t, value=v)

class XVariableInfoWithXVId(XVariableInfoDTO):
    xvid:str
    @staticmethod
    def from_xvariableinfo(x:XVariableInfoDTO):
        return XVariableInfoWithXVId(type= x.type, value = x.value, xvid=x.calculate_hash())
    

class TemporalVariableInfo(BaseModel):
    type: str
    xfrom: Optional[int] = 0
    xto: Optional[int] = 0
    value: Optional[str] =""
    def calculate_hash(self):
        for i in range(self.xfrom, self.xto+1):
            h = H.sha256()
            x = f"{self.type}{i}".encode()
            h.update(x)
            yield h.hexdigest()
        xx = f"{self.type}{self.xfrom}{self.xto}".encode()
        h = H.sha256()
        h.update(xx)
        yield h.hexdigest()
class TemporalVariableInfoWithXVId(TemporalVariableInfo):
    xvid:List[str]
    @staticmethod
    def from_tv_info(x:TemporalVariableInfo):
        return TemporalVariableInfoWithXVId(type= x.type, xfrom=x.xfrom,xto=x.xto,xvid=list(x.calculate_hash()))


class SVResult(BaseModel):
    variable_type: str
    elements: List[List[XVariableInfoDTO]]
    # def calci
    def calculate_hashes(self)->Generator[XVariableMultipleInfoWithXVId,None,None]:
        for es in self.elements:
            h = H.sha256()
            _type = ""
            _value = ""
            xvi_mul = XVariableMultipleInfoWithXVId()
            for e in es:
                x = f"{e.type}{e.value}".encode()
                h.update(x)
                _type+=e.type
                _value+=e.value
                xvi_mul.types.append(e.type)
                xvi_mul.values.append(e.value)
                
            xvi_mul. xvid=h.hexdigest()
            yield xvi_mul

class TVResult(BaseModel):
    variable_type: str
    elements: Optional[List[TemporalVariableInfo]] = []
    def calculate_hashes(self)->Generator[TemporalVariableInfoWithXVId,None,None]:
        for e in self.elements:
            x = TemporalVariableInfoWithXVId.from_tv_info(e)
            yield x

class IVResult(BaseModel):
    variable_type: str
    elements: List[XVariableInfoDTO]
    def calculate_hashes(self)->Generator[XVariableInfoWithXVId,None,None]:
        for e in self.elements:
            yield XVariableInfoWithXVId.from_xvariableinfo(e)

class PTResult(BaseModel):
    variable_type:str 
    elements: List[XVariableInfoDTO]
    def calculate_hashes(self)->Generator[XVariableInfoWithXVId,None,None]:
        for e in self.elements:
            yield XVariableInfoWithXVId.from_xvariableinfo(e)

class InterpretedResult(BaseModel):
    sv: SVResult
    tv: TVResult
    iv: IVResult
    pt: PTResult