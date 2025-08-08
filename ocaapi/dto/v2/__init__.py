from typing import Optional,List,Tuple, Any,Generator,Dict
from pydantic import BaseModel
from ocaapi.models.v2 import XVariableModel,XVariableType,XType
# import ocaapi.querylang.peg as qlx
import json as J
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
    description:Optional[str]="No description yet."
    type: str
    xtype:Optional[XType] = XType.X
    variable_type:Optional[XVariableType] = None
    raw: Optional[str] =""
    order: Optional[int] = -1 
    value: Any
    
    def build(self):
        try:
            hasher          = H.sha256()
            self.type = self.type.upper()
            
            hasher.update(self.type.encode("utf-8"))
            if self.xtype == XType.String or self.xtype == XType.Float or self.xtype == XType.Integer or self.xtype == XType.X:
                if self.xtype == XType.String:
                    self.value = self.value.upper()

                xbytes         = f"{self.value}".encode("utf8")
                self.raw=f"{self.type}({self.value})"
                hasher.update(xbytes)
            elif self.xtype == XType.Array:
                str_xs = list(map(lambda x: str(x).upper(), self.value))
                self.value = str_xs
                xs = "".join(str_xs)
                
                self.raw= f"{self.type}({str(str_xs) })"
                hasher.update(xs.encode("utf-8"))

            elif self.xtype == XType.Date:
                date_str = self.value.isoformat()
                self.raw = f"{self.type}({self.value.month},{self.value.day},{self.value.year})"
                hasher.update(date_str.encode("utf-8"))
            elif self.xtype == XType.DateRange:
                _start = self.value["start"]
                _end  = self.value["end"]
                start_date = _start.isoformat()
                end_date   = _end.isoformat()
                left_open  = self.value["left_open"]
                right_open = self.value["right_open"]
                left       = "(" if left_open else "["
                right      = ")" if right_open else "]"
                x = f"{left}{start_date}{end_date}{right}"
                self.raw = f"{left}Date({_start.month},{_start.day},{_start.year}),Date({_end.month},{_end.day},{_end.year}){right}"
                hasher.update(x.encode("utf-8"))
            elif self.xtype == XType.IntegerRange or self.xtype == XType.Range:
                start = self.value["start"]
                end   = self.value["end"]
                step  = self.value.get("step",1)
                left_open  = self.value["left_open"]
                right_open = self.value["right_open"]
                left       = "(" if left_open else "["
                right      = ")" if right_open else "]"
                x     = f"{left}{start}{end}{step}{right}"
                self.raw = f"{left}{self.type}({start},{end},{step}){right}"
                hasher.update(x.encode("utf-8"))
            elif self.xtype == XType.Object:
                normalized_data = J.dumps(self.value,sort_keys=True)
                data_bytes = normalized_data.encode("utf-8")
                hasher.update(data_bytes)
            xvid             = hasher.hexdigest()
            self.xvid = xvid
        except Exception as e:
            print(f"Error building the Xvariable, please check the format: {e}")

    @staticmethod
    def from_model(x:XVariableModel)->'XVariableDTO':
        return XVariableDTO(
            **x.model_dump()
        )

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


class XVariableParentRelationshipDTO(BaseModel):
    parent_id: str
    child_id: str

 
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