from ocaapi.repositories.v2 import ObservatoriesRepository,XVariablesRepository,ProductRepository,XVariableAssignmentRepository
from ocaapi.models.v2 import XVariableModel,ObservatoryModel,ProductModel,XVariableAssignment,ContentVars,PlotDescription,ContextualVariables
from ocaapi.dto.v2 import ObservatoryDTO,XVariableDTO,ProductDTO,MultipleXVariableAssignmentDTO,ManyProductsMultipleXVariableAssignmentDTO,XVariableRawAssignmentDTO,ProductCreationDTO,SVResult,TVResult,IVResult,PTResult,XVariableInfoDTO,TemporalVariableInfo,ProductFoundDTO,XVariableMultipleInfoWithXVId
from option import Result,Ok,Err
from nanoid import generate as nanoid
from ocaapi.errors import OcaError,UknownError,NotFound,AlreadyExists
from typing import List,Tuple,Dict,Any,Coroutine
import hashlib as H
import asyncio
# from hashlib import _Hash
from ocaapi.querylang.peg import parse,parse_sv,parse_pt,parse_iv,parse_tv

class OcaNameService:
    def __init__(self, 
        xvariable_assignments_repo:XVariableAssignmentRepository,
        product_repo: ProductRepository
    ):
        self.xvariable_assignments_repo = xvariable_assignments_repo
        self.product_repo = product_repo

    async def filter(self, query:str,strict:bool = False):
        try: 
            # print("QUERY",query)
            res = parse(query).asDict()
            sv  = res.get("sv")
            sv  = SVResult(**sv) if sv else None
            tv  = res.get("tv") 
            # print("TV",tv)
            tv  = TVResult(**tv) if tv else None
            iv  = res.get("iv")
            iv  = IVResult(**iv) if iv else None
            ov  = res.get("ov")
            
            pt  = res.get("pt")
            pt  = PTResult(**pt) if pt else None
            xxs = list(sv.calculate_hashes())
            ys  = list(tv.calculate_hashes())
            ws  = list(iv.calculate_hashes())

            sv_found_products:List[str] = []
            for x in xxs:
                _query = {"xvid":x.xvid}
                result = await self.xvariable_assignments_repo.find(query=_query)
                if result.is_err:
                    continue
                results = result.unwrap()
                for y in results:
                    if not y.xid in sv_found_products:
                        sv_found_products.append(y.xid)

            tv_found_products:List[str] = []
            for y in ys:
                for xvid in y.xvid:
                    _query = {"xvid":xvid}
                    result = await self.xvariable_assignments_repo.find(query=_query)
                    if result.is_err:
                        continue
                    results = result.unwrap()
                    for r in results:
                        if not r.xid in tv_found_products:
                            tv_found_products.append(r.xid)
            
            for w in ws:
                print("W",w)
            print("SV_FP", sv_found_products)
            print("TV_FP",tv_found_products)

            
                # print("Y",y)

            # for (i, p) in found_products:
            # async def run_and_keep(cr: Coroutine[Any, Any, Result[ProductDTO, Exception]], x):
            #     result = await cr
            #     return result,x
            # products = [ run_and_keep(self.product_repo.find_by_pid(pid= i), xvm) for (i,xvm) in found_products]
            # products:List[Tuple[Result[ProductDTO,Exception],XVariableMultipleInfoWithXVId]] = await asyncio.gather(*products)
            # products = list(map(lambda x: (x[0].unwrap(),x[1]),filter(lambda x: x[0].is_ok, products)))
            # pfs = []
            # for (p,xvm) in products:
            #     pf = ProductFoundDTO(
            #         pid = p.pid,
            #         description=p.description,
            #         name= p.name,
            #         tags= list(xvm.to_tags()),
            #     )
            #     pfs.append(pf)
            pfs = []
            return pfs
        except Exception as e:
            print("ERROR",e)
            # return Err(e)
            # print("RESULTS",results)
                
            #     resp = result.unwrap()
            #     if not resp.xid in found_products:
            #         # print("PRODUCT",product)
            #         temp_xid = resp.xid
            #         # found_products.append(resp.xid)
            #         matches+=1
            #     else:
            #         matches+=1
            # print("MATCHES", matches)
            # if matches == len(xs):
            #     print("_"*20)
            #     print("MATCHES", temp_xid)
            #     print("xs",xs)
            #     print("_"*20)
            #     found_products.append(temp_xid)
            # temp_xid= ""
            # matches=0
            
                    # print()
                    
            
            # print(resp.xid)
            # print("RESULT", result)

        # print("XS",xs)
        # ys = list(tv.calculate_hashes())
        # print("YS",ys)
        # ws = list(iv.calculate_hashes())
        # print("WS",ws)
        # zs  = list(pt.calculate_hashes())
        # print("ZS",zs)
        

class ObservatoriesService:
    def __init__(self, repo: ObservatoriesRepository):
        self.repo = repo
        self.obid_aphabet = "0123456789abcdefghijklmnopqrst"
        self.obid_size = 10

    async def create(self, observatory: ObservatoryDTO) -> Result[str, OcaError]:
        try:
            y = observatory.model_dump()
            print("Y",y)
            obs_model = ObservatoryModel(**y)
            if obs_model.obid == "":
                obs_model.obid = f"obs-{nanoid(alphabet=self.obid_aphabet, size=self.obid_size)}"
                
            x = await self.repo.create(obs_model)
            if x.is_err:
                return Err(UknownError(detail="Observatory creation failed."))
            return Ok(obs_model.obid)
        except Exception as e:
            return Err(e)

    async def find_by_obid(self, obid: str) -> Result[ObservatoryModel, OcaError]:
        try:
            x = self.repo.find_by_obisd(obid=obid)
        except Exception as e:
            return Err(e)

    async def update_observatory(self, obid: str, dto: ObservatoryDTO) -> bool:
        return await self.repo.update(obid, dto.model_dump())

    async def delete_observatory(self, obid: str) -> bool:
        return await self.repo.delete(obid)

class XVariablesService:
    def __init__(self, repo: XVariablesRepository):
        self.repo = repo

    async def create(self, xvariable: XVariableDTO) -> Result[str, OcaError]:
        try:
            hasher          = H.sha256()
            if xvariable.xvid == "":
                xbytes         = f"{xvariable.type}{xvariable.value}".encode("utf8")
                hasher.update(xbytes)
                xx             = hasher.hexdigest()
                xvariable.xvid = xx
            
            exists = await self.find_by_xvid(xvid=xvariable.xvid)
            if exists.is_ok:
                return Err(AlreadyExists(detail="XVariable already exists."))

            
            y = xvariable.model_dump()
            model = XVariableModel(**y)
            x     = await self.repo.create(model)
            if x.is_err:
                return x
            return Ok(model.xvid)
        except Exception as e:
            return Err(e)

    async def find_by_xvid(self, xvid:str)->Result[XVariableDTO, OcaError]:
        try:
            x = await self.repo.find_by_xvid(xvid=xvid)
            if x.is_err:
                return Err(NotFound(detail=str(x.unwrap_err())))
            xx = x.unwrap()
            return Ok(XVariableDTO.from_model(xx))
        except Exception as e: 
            return Err(e)
    
    async def find_by_type_values(self,
        type:str, 
        values:List[str]=[]
    )->Result[XVariableDTO,OcaError]:
        try:
            xvids = []
            for value in values:
                x      = f"{type}{value}"
                hasher = H.sha256()
                hasher.update(x.encode("utf-8"))
                xvid   = hasher.hexdigest()
                xvids.append(xvid)
            res    = await self.repo.find_by_xvids(xvids)
            if res.is_err:
                return Err(UknownError(detail=str(res.unwrap_err())))
            
            return Ok(res.unwrap())
        except Exception as e: 
            return Err(e)
    # async def get_variables_by_parent(self, parent_id: str) -> Result[list[XVariableModel], OcaError]:
    #     return self.repo.find_by_parent_id(parent_id)

    # async def update_variable(self, obid: str, dto: XVariableDTO) -> bool:
    #     return self.repo.update(obid, dto.dict())

    # async def delete_variable(self, obid: str) -> bool:
    #     return self.repo.delete(obid)
    

class ProductsService:
    def __init__(self, 
        repo: ProductRepository,
        xvar_repo: XVariablesRepository,
        xvar_assignments_repo:XVariableAssignmentRepository,
    ):
        self.repo                  = repo
        self.xvar_assignments_repo = xvar_assignments_repo
        self.xvar_repo             = xvar_repo
        self.obid_aphabet          = "0123456789abcdefghijklmnopqrst"
        self.obid_size             = 10
    
    @staticmethod
    def __sv_assignments(h_pid:"H.Hash", elements:List[List[XVariableInfoDTO]])->Tuple[List[XVariableAssignment],List[XVariableModel], "H.Hash"]:
        pid = ""
        sv_assignments:List[XVariableAssignment] = []
        xvid_models:List[XVariableModel] = []
        for sv_inner_elements in elements:
            h_seq = H.sha256()
            current_parent_id = ""
            for sv_element in sv_inner_elements:
                h = H.sha256()
                xvid_bytes = f"{sv_element.type}{sv_element.value}".encode()
                h.update(xvid_bytes)
                h_seq.update(xvid_bytes)
                h_pid.update(xvid_bytes)
                # 
                xvid = h.hexdigest()
                xvariable_model = XVariableModel(
                    xvid=xvid,
                    description="",
                    type=sv_element.type, 
                    value=sv_element.value, 
                    parent_id=current_parent_id
                )
                xvid_models.append(xvariable_model)
                current_parent_id = xvid
                sv_assignments.append(XVariableAssignment(xid=pid, xvid=xvid))
            xvid_seq = h_seq.hexdigest()
            sv_assignments.append(XVariableAssignment(xid=pid, xvid=xvid_seq))
        return sv_assignments,xvid_models, h_pid
    
    @staticmethod
    def __tv_assignments(h_pid:"H.Hash", elements:List[TemporalVariableInfo])->Tuple[List[XVariableAssignment],List[XVariableModel], "H.Hash"]:
            tv_assigments = []
            tv_elements = sorted(elements, key=lambda x: x.xfrom+x.xto)
            pid = ""
            xvariable_models:List[XVariableModel] = []
            for tv_element in tv_elements:
                _type            = tv_element.type
                h_tv_complete    = H.sha256()
                h_tv_years_full  = H.sha256()
                xvid_years_bytes = f"{_type}{tv_element.xfrom}{tv_element.xto}".encode()
                h_tv_years_full.update(xvid_years_bytes)
                tv_assigments.append(XVariableAssignment(xid=pid, xvid= h_tv_years_full.hexdigest()))
                for i in range(tv_element.xfrom, tv_element.xto+1):
                    h_vt = H.sha256()
                    xvid_bytes = f"{_type}{i}".encode()
                    # 
                    h_vt.update(xvid_bytes)
                    h_tv_complete.update(xvid_bytes)
                    h_pid.update(xvid_bytes)
                    # 
                    xvid = h_vt.hexdigest()
                    xvariable_model = XVariableModel(
                        xvid        = xvid,
                        description = "",
                        parent_id   = "",
                        type        = tv_element.type,
                        value       = f"{i}",
                    )
                    xvariable_models.append(xvariable_model)
                    tv_assigments.append(XVariableAssignment(xid=pid, xvid=xvid))
                xvid_global = h_tv_complete.hexdigest()
                xvariable_models.append(
                    XVariableModel(
                        xvid        = xvid_global,
                        description = "",
                        parent_id   = "",
                        type        = tv_element.type,
                        value       = f"{tv_element.xfrom}_{tv_element.xto}",
                    )
                )
                tv_assigments.append(XVariableAssignment(xid=pid, xvid=xvid_global))
            return tv_assigments,xvariable_models,h_pid

    @staticmethod
    def __iv_assignments(h_pid:"H.Hash", elements:List[XVariableInfoDTO])->Tuple[List[XVariableAssignment],List[XVariableModel], "H.Hash"]:
        iv_assigments = []
        h_iv_global = H.sha256()
        iv_elements = sorted(elements, key=lambda x: x.value)
        pid = ""
        xvar_models:List[XVariableModel] = []
        for iv_element in iv_elements:
            h_iv = H.sha256()
            xvid_bytes =f"{iv_element.type}{iv_element.value}".encode() 
            # Hashes
            h_iv.update(xvid_bytes)
            h_iv_global.update(xvid_bytes)
            h_pid.update(xvid_bytes)
            # 
            xvid = h_iv.hexdigest()
            xvar_model = XVariableModel(
                xvid=xvid,
                description="",
                parent_id="",
                type=iv_element.type,
                value=iv_element.value,
            )
            xvar_models.append(xvar_model)
            iv_assigments.append(XVariableAssignment(xid=pid, xvid=xvid))
        xvid_global = h_iv_global.hexdigest()
        iv_assigments.append(XVariableAssignment(xid=pid, xvid=xvid_global))
        return iv_assigments,xvar_models, h_pid

    @staticmethod
    def __pt_assignments(h_pid: "H.Hash", elements:List[XVariableInfoDTO])->Tuple[List[XVariableAssignment],List[XVariableModel], "H.Hash"]:
        h_pt_global = H.sha256()
        pt_assigments = []
        pid = ""
        xvar_models:List[XVariableModel] = []
        for pt_element in elements:
            h_pt = H.sha256()
            xvid_bytes = f"{pt_element.type}{pt_element.value}".encode()
            # 
            h_pt.update(xvid_bytes)
            h_pt_global.update(xvid_bytes)
            h_pid.update(xvid_bytes)
            #
            xvid = h_pt.hexdigest()
            xvar_model = XVariableModel(
                xvid= xvid, 
                description="",
                parent_id="",
                type=pt_element.type,
                value=pt_element.value,
            )
            xvar_models.append(xvar_model)
            pt_assigments.append(XVariableAssignment(xid=pid, xvid=xvid))

        xvid_global = h_pt_global.hexdigest()
        pt_assigments.append(XVariableAssignment(xid=pid, xvid=xvid_global))
        return pt_assigments,xvar_models, h_pid

    async def createx(self, product: ProductCreationDTO) -> Result[str, OcaError]:
        try:
            sv_result = SVResult(**parse_sv(f"SV={product.ctx_vars.spatial_var}").asDict().get("sv"))
            tv_result = TVResult(**parse_tv(f"TV={product.ctx_vars.temporal_var}").asDict().get("tv"))
            iv_result = IVResult(**parse_iv(f"IV={product.content_vars.interest_var}").asDict().get("iv"))
            pt_result = PTResult(**parse_pt(f"ProductType={product.ctx_vars.product_type}").asDict().get("pt"))
            
            pid = ""
            h_pid = H.sha256()
            sv_assignments,sv_xvar_models, h_pid = ProductsService.__sv_assignments(h_pid=h_pid, elements=sv_result.elements)
            # print(sv_xvar_models)
            # _____________________________A
            # TV ASSIGMENTS
            tv_assigments,tv_xvar_models,h_pid = ProductsService.__tv_assignments(h_pid=h_pid, elements=tv_result.elements)
            # print(tv_xvar_models)
            #  IV ASSIGMENTS
            iv_assigments,iv_xvar_models,h_pid = ProductsService.__iv_assignments(h_pid=h_pid, elements=iv_result.elements)
            # print("IV_MODELS",iv_xvar_models)
            pt_assignments,pt_xvar_models,h_pid = ProductsService.__pt_assignments(h_pid=h_pid, elements=pt_result.elements)
            # print("PT_MODELS",pt_xvar_models)
            # print("PT_ASSIGMENTS", pt_assignments)
            pid = h_pid.hexdigest()
            
            assignments = sv_assignments + tv_assigments + iv_assigments + pt_assignments
            assignments_with_error:List[XVariableAssignment]  = []
            xvar_models = sv_xvar_models + tv_xvar_models + iv_xvar_models + pt_xvar_models

            xvar_with_error:List[XVariableModel] = []
            for xvar_model in  xvar_models:
                exists = await self.xvar_repo.exists_by_xvid(xvid=xvar_model.xvid)
                if exists:
                    continue
                res = await self.xvar_repo.create(variable=xvar_model)
                if res.is_err:
                    xvar_with_error.append(xvar_model)
            
            if len(xvar_models) == len(xvar_with_error):
                xvar_with_error = []

            for x in assignments:
                x.xid = pid
                exists = await self.xvar_assignments_repo.exists_by_xid_and_xvid(xid=x.xid, xvid=x.xvid)
                if not exists:
                    res = await self.xvar_assignments_repo.create(x)
                    if res.is_err:
                        print(x,res, "Failed to save")
                        assignments_with_error.append(x)
            if len(assignments_with_error) == len(assignments):
                assignments_with_error = []
            
            product_model = ProductModel(
                pid            = pid,
                name           = product.name,
                description    = product.description,
                data_source_id = product.data_source_id,
                data_view_id   = product.data_view_id,
                content_vars   = ContentVars(**product.content_vars.model_dump()),
                ctx_vars       = ContextualVariables(**product.ctx_vars.model_dump()),
                plot_desc      = PlotDescription(**product.plot_desc.model_dump()),
                disabled       = False,
            )
            product_exists = await self.repo.exists_by_pid(pid=pid)
            if not product_exists:
                result = await self.repo.create(product=product_model)
                if result.is_err:
                    return Err(UknownError(detail=str(result.unwrap_err())))
            return Ok(pid)
        except Exception as e:
            return Err(e)
    # async def create(self, product: ProductCreationDTO) -> Result[str, OcaError]:
    #     try:
    #         if product.pid  == "":
    #             product.pid = nanoid(alphabet=self.obid_aphabet, size=self.obid_size)
    #         exists = await self.repo.find_by_pid(pid= product.pid)
    #         if exists.is_ok:
    #             return Err(AlreadyExists("Product already exists."))
    #         product_model = ProductModel(
    #             pid            = ,
    #             name           = product.name,
    #             description    = product.description,
    #             data_source_id = product.data_source_id,
    #             data_view_id   = product.data_view_id,
    #             content_vars   = ContentVars(**product.content_vars),
    #             ctx_vars       = ContextualVariables(**product.ctx_vars),
    #             plot_desc      = PlotDescription(**product.plot_desc),
    #             disabled       = False,
    #         )
    #         # model = ProductModel(**product.model_dump())
    #         x = await self.repo.create(model)
    #         return Ok(product.pid)
    #     except Exception as e:
    #         return Err(e)
    
class XVariableAssignmentsService:
    def __init__(self, repo: XVariableAssignmentRepository):
        self.repo = repo

    async def assign(self,dto:MultipleXVariableAssignmentDTO)->Result[List[str],OcaError]:
        try:
            xid = dto.xid
            xvids = []
            for assignment in dto.assignments:
                h = H.sha256()
                x = f"{assignment.kind}{assignment.value}"
                h.update(x.encode("utf-8"))
                xvid = h.hexdigest()
                xvids.append(XVariableAssignment(xid=xid, xvid=xvid))
            res = await self.repo.create_many(xs=xvids)
            if res.is_err:
                return Err(UknownError(detail=str(res.unwrap_err())))
            return res
        except Exception as e:
            return Err(e)

