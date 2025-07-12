from pyparsing import ParserElement,ParseResults
from typing import Set,Dict,Any
import calendar
from datetime import datetime
import hashlib as H


class InfoParseActions:

    def parse(tks:ParserElement):
        val = tks.get("value")
        print("INFO_PARSE",tks)
        return {
            "variable_type":tks.get("variable_type","UKNOWN"),
            "elements":val.asList()
        }

    @staticmethod
    def parse_ivs_values(tks:ParserElement):
        values = tks.asList()
        xs = []
        for v in values:
            __values = v.get("value")
            h = H.sha256()
            _type = v.get("type").upper()
            for _v in __values:
                h.update(f"{_type.upper()}{_v.upper()}".encode())
            # __values = __values.upper()
            xvid = h.hexdigest()
            xs.append({
                "xvid":xvid,
                "type":_type,
                "value":__values,
                "xtype":"ARRAY"
            })
 
                
        return xs
    @staticmethod
    def parse_value(tks:ParserElement):
        print("INFO_VALUE",tks)
        return [tks]
    @staticmethod
    def parse_info_ivs(tks:ParserElement):
        values = tks.asList()
        # print("INFO_IVS",values)
        # for x in values:
            # h = H.sha256()
            # vs = x.get("xvid")
            # h.update(vs.encode())
        # x["xvid"] = h.hexdigest()
            # print("X",x)
        return [values]
        # return {
        #     "type":"INTEREST",
        #     "values":values,
        #     # "xvid":xvid
        # }
    @staticmethod
    def parse_info_iv(tks:ParserElement):
        # print("TKLS_INFO_IV",tks)
        _type = tks.get("iv_type")
        value = tks.get("iv_value")
        # print("IV_VALUE",value)
        h = H.sha256()
        for v in value:
            h.update(f"{_type}{v}".encode())

        return {
            "xvid":h.hexdigest(),
            "type":_type.upper(),
            "value":list(map(lambda x:x.upper(),value)),
            "xtype":"STRING"
        }
    @staticmethod
    def parse_stats(tks:ParserElement):
        name = tks.get("stat_name","UKNOWN")
        val  = tks.get("stat_value","0")
        return {"type":name, "value":float(val)}

    @staticmethod
    def parse_info_element(tks:ParserElement):
        event   = tks.get("event").upper()
        ov      = tks.get("ov").upper()
        print("PARSE_INFO_ELEMENT_TKS",tks)
        scale   = tks.get("scale","").upper()
        # iv_type = tks.get("iv_type")
        # iv_val  = tks.get("iv_value")
        stat    = tks.get("stat")
        interest = tks.get("interest").asList()
        stat_type = stat.get("type").upper()
        stat_value = stat.get("value")
        xvid_str = f"{event}{ov}{scale}{stat_type}{stat_value}"
        for i in interest:
            xvid_str+=i.get("xvid")
        h = H.sha256()
        h.update(xvid_str.encode())
        return {
            "xvid":h.hexdigest(),
            "event":event,
            "method":ov,
            "scale":scale,
            "interest":interest,
            "stat":stat_type,
            "value": stat_value
        }

    @staticmethod
    def parse_info_query(tks:ParserElement):
        print("PASRSE_INFO_QUERY", tks )
        return tks
    @staticmethod
    def parse_info_query_value(tks:ParserElement):
        print("PARSEa_INFO_QUERY_VALUE",list(tks.keys()))
        left       = tks.get("left")
        right      = tks.get("right")
        print("LEFT",list(left.keys()))
        print(dir(left),list(left.values()))


    @staticmethod
    def parse_info_query_left(tks:ParserElement):
        print("LEFT",list(tks.keys()))
        ov = tks.get("ov")
        iv_type = tks.get("iv_type")
        iv_value = tks.get("iv_value")
        print("OV",ov)
        print("iv_type",iv_type)
        print("iv_value",iv_value)
        return tks
        # print(left.asList()[0].keys())
        # print("RIFHT",right)
        # iv_type  = tks.get("iv_type")
        # iv_value = tks.get("iv_value")
        # print("OV",ov)
        # print("IV_TYPE",iv_type)
        # print("IV_VALUIE",iv_value)
        # return tks

class ObservableParseActions:

    @staticmethod
    def parse_ov_element(tks:ParserElement):
        values = tks.asList()
        # print("PRASE_ELEMENT",tks)
        event  = values[0].upper()
        method = values[1].upper()
        scale  = ("" if len(values) < 3 else values[2]).upper()
        h = H.sha256()
        x = f"{event}{method}{scale}".encode()
        h.update(x)
        return {
            "type":"OBJECT",
            "xvid":h.hexdigest(),
            "value":{
                "event":event,
                "method":method,
                "scale":scale
            },
            "xtype":"OBJECT",
        }
   
    @staticmethod
    def parse_value(tks:ParserElement):
        values = tks.asList()
        return values

    @staticmethod
    def parse(tks:ParserElement):
        tks_list = tks.asList()
        elements = list(filter(lambda x: isinstance(x, dict), tks_list))
        return {"variable_type": "OV", "elements":elements}

class ProductTypeParseActions:
    @staticmethod
    def parse(tks:ParserElement):
        tks_list = tks.asList()
        elements = list(filter(lambda x: isinstance(x, dict), tks_list))
        # print("TKS",elements)
        return {"variable_type":"PT","elements":elements}

    # @staticmethod
    # def hash():

    @staticmethod
    def parse_value(tks:ParserElement):
        values =  tks.asList()
        v_len = len(values)
        if v_len ==1:
            if values[0] =="*":
                return [{"type":"Wildcard".upper(), "value":"*"}]
        elements = []
        for v in values:
            _type = "ProductType".upper()
            value = v.upper()
            h = H.sha256()
            h.update(f"{_type}{value}".encode())
            elements.append({
                "xvid":h.hexdigest(),
                "type":_type, 
                "value":value,
                "xtype":"STRING"
            })
        return elements

class InterestVariableParseActions:
    @staticmethod
    def parse(tks:ParserElement):
        # print("*"*20)
        variable_type = tks.get("variable_type","UKNOWN")
        # value_:ParseResults = tks.get("value",[])
        # value = value_.asList()
        tks_list = tks.asList()
        elements = list(filter(lambda x: isinstance(x, dict), tks_list))
        return {"variable_type":variable_type,"elements":elements }
    
    @staticmethod
    def parse_iv_hierarchy_element(tks:ParserElement):
        # print("IV_HIERARCHY_ELEMENT", tks,list(tks.keys()))
        _type = tks.get("type","")
        value = tks.get("value")
        h = H.sha256()
        h.update(f"{_type}{value}".encode())
        xvid  = h.hexdigest()
        return {
            "type":_type,
            "value":value,
            "xtype":"STRING",
            "xvid":xvid
        }
    @staticmethod
    def parse_iv_hierarchy(tks:ParserElement):
        values = tks.asList()
        h_global = H.sha256()
        for v in values:
            # print("VALUEEEE",v)
            xvid:str   = v.get("xvid")
            h_global.update(xvid.encode())

        return {
            "type":"SEQUENCE",
            "values":values,
            "xvid":h_global.hexdigest()
        }
    
    @staticmethod
    def parse_element(tks:ParserElement):
        value = tks.get("value","VALUE").asList()
        type_ = tks.get("type","TYPE").upper()

        _value = list(map(lambda x:x.upper(),list(set(value))))
        _value = sorted(_value, key= lambda k:k)
        values = []
        h_g = H.sha256()
        # print("PARSE_ELEMENTTTTTTTTTTTTTTTTTTTTT",_value)
        for v in _value:
            h  = H.sha256()
            x = f"{type_}{v}".encode()
            h.update(x)
            h_g.update(x)
            xvid = h.hexdigest()
            values.append({"type":type_, "value":v, "xvid":xvid,"xtype":"STRING"})
        return { 
            "type": "ARRAY", 
            "values": values,
            "xvid":h_g.hexdigest(),
            "xtype":"ARRAY"
        }
    
    @staticmethod
    def parse_value(tks:ParserElement):
        vs = tks.get("value",[])
        v_len = len(vs)
        # print("IV_VALUE", tks)
        # print("VS",vs)
        # print("*"*20)
        if v_len ==1:
            if vs[0] =="*":
                xvid = ""
                return [{"type":"WILDCARD", "value":"*","xvid":xvid}]
        


        return tks
    @staticmethod
    def parse_iv_ranges(tks:ParserElement):
        # print("IV_RANGES_TKS",tks,list(tks.keys()))
        # This must be replaced in the future, for now is nice... 
        a = tks.get("a")
        b = tks.get("b")
        a_float = float(a)
        b_float = float(b)
        a_int = int(a_float)
        b_int = int(b_float)
        a_x = a_float - a_int
        b_x = b_float - b_int
        is_float = a_x >0 or b_x >0
        h          = H.sha256()
        _type      = tks.get("type")
        start      = a_float if is_float else a_int
        end        = b_float if is_float else b_int
        left_open  = "lopen" in tks
        right_open = "ropen" in tks
        value = f"{_type}{int(left_open)}{start}{end}{int(right_open)}"
        # print("VALUE",value)
        h.update(value.encode())
        return {
            "type":_type,
            "left_open": left_open,
            "right_open": right_open,
            "start":start,
            "end": end,
            "xtype": "Range" if is_float  else "IntegerRange",
            "xvid":h.hexdigest()
        }

class TemporalVariableParseActions:
    MONTH_TO_INT = {
        "january"  : 1,  "jan": 1,
        "february" : 2,  "feb": 2,
        "march"    : 3,  "mar": 3,
        "april"    : 4,  "apr": 4,
        "may"      : 5,
        "june"     : 6,  "jun": 6,
        "july"     : 7,  "jul": 7,
        "august"   : 8,  "aug": 8,
        "september": 9,  "sep": 9,  "sept": 9,
        "october"  : 10, "oct": 10,
        "november" : 11, "nov": 11,
        "december" : 12, "dec": 12
    }
    INT_TO_STR_MONTH = {
        1: ("January", "Jan"),
        2: ("February", "Feb"),
        3: ("March", "Mar"),
        4: ("April", "Apr"),
        5: ("May", "May"),
        6: ("June", "Jun"),
        7: ("July", "Jul"),
        8: ("August", "Aug"),
        9: ("September", "Sep"),
        10: ("October", "Oct"),
        11: ("November", "Nov"),
        12: ("December", "Dec")
    }
    MIN_YEAR = 1970

    @staticmethod
    def parse(tks):
        return {
            "variable_type":tks.get("variable_type","UKNOWN_VARIABLE"), 
            "elements": tks.get("value",[]).asList()
        }

    @staticmethod
    def parse_tv_range(tks:ParserElement):
        a = tks.get("a")
        b = tks.get("b")
        # __________________
        a_year  = a.get("year")
        a_month = a.get("month")
        a_day   = a.get("day")
        # __________________
        b_year  = b.get("year")
        b_month = b.get("month")
        b_day   = b.get("day")
        # __________________
        a_month_index = a_month.get("index")
        b_month_index = b_month.get("index")
        left_open = "lopen" in tks
        right_open = "ropen" in tks
        x = f"{left_open}{a_month}{a_day}{a_year}{b_month}{b_day}{b_year}{right_open}"
        h       = H.sha256()
        h.update(x.encode())
        return {
            "type":"DATE_RANGE",
            "start":datetime(a_year, a_month_index, a_day),
            "end":datetime(b_year, b_month_index, b_day),
            "left_open": left_open,
            "right_open": right_open,
            "xvid":h.hexdigest(),
            "xtype":"DATE_RANGE"
        }
    @staticmethod
    def parse_range_value(tks:ParserElement):
        # print("TV_RANGE_VALUE",list(tks.keys()))
        return {
            "type":tks.get("type"),
            "month":tks.get("month"),
            "day":tks.get("day"),
            "year":tks.get("year")
        }


    @staticmethod
    def parse_value(tks:ParserElement):
        # print("TKS",tks)
        return tks
    @staticmethod
    def parse_tv_element(tks:ParserElement):
        keys = list(tks.keys())
        # print("_"*20)
        # print("KEYS",keys)
        if len(keys) ==1 and "value" in keys:
            return {"type": "WILDCARD", "value":"*"}
        else:
            type = tks.get("type").upper()
            month = tks.get("month")
            day   = tks.get("day")
            year = tks.get("year")
            # print("MONTH",month)
            # print("DAY",day)
            if day == 0 and month.get("index",0) ==0:
                h = H.sha256()
                h.update(f"{type}11{year}".encode())
                return { 
                    "type":type, 
                    "value": datetime(year=year, month=1, day=1),
                    "xvid":h.hexdigest()
                }
            
            _,days_in_month = calendar.monthrange(year=year, month=month.get("index",0))
            if day > days_in_month:
                raise Exception(f"days must be between 1 and {days_in_month}")
            # print(f"{days_in_month} IN {month.get('short_name')} ")
            h = H.sha256()
            h.update(f"{type}{month}{day}{year}".encode())
            return { "type":type, 
                    "value":datetime(year=year, month=month.get("index"),day=day),
                    "xvid":h.hexdigest()
                    # "month": month.get("index"), "day":day, "year":year
                }
    @staticmethod
    def parse_tv_month(tks:ParserElement):
        # print("TKS_PARVTV_MONTHJ",tks,list(tks.keys()))
        month = tks.get("month")
        if "int_month" in tks:
            _month    = int(month)
            if _month == 0:
                return {
                    "type":"MONTH",
                    "index":_month,
                    "full_month_name":"",
                    "short_month_name":""
                }
            if _month <0:
                raise Exception("Month cannot be lower than 0.")
            elif _month > 12:
                raise Exception("Month cannot be greater to 12")
            else:
                x = TemporalVariableParseActions.INT_TO_STR_MONTH.get(_month)
                return {
                    "type":"Month",
                    "index":_month,
                    "full_name":x[0].upper(),
                    "short_name":x[1].upper()
                }
        else:
            _month = TemporalVariableParseActions.MONTH_TO_INT.get(month)
            x = TemporalVariableParseActions.INT_TO_STR_MONTH.get(_month)
            return {
                "type":"MONTH",
                "index":_month,
                "full_month_name":x[0].upper(),
                "short_month_name":x[1].upper()
            }
    def parse_tv_day(tks:ParserElement):
        # print("TKS_PARVTV_DAY",tks,list(tks.keys()))
        return int(tks.get("day",0))
    def parse_tv_year(tks:ParserElement):
        # print("TKS_PARVTV_YEAR",tks,list(tks.keys()))
        year = int(tks.get("year",0))
        if year <= 0 :
            raise Exception("Year must be greater than 0")
        if year <TemporalVariableParseActions.MIN_YEAR:
            raise Exception("Year must be greater than 1970")
        return year
    @staticmethod
    def _parse_value(tks:ParserElement):
        value = tks.get("value",[])
        v_len = len(value)
        # print("TEM<PORAL", value)
        if v_len ==1:
            if value[0] =="*":
                return [{"type":"WILDCARD", "value":"*"}]
        return tks
    @staticmethod
    def parse_years(tks:ParserElement):
        xfrom = int(tks.get("from",0))
        xto   = int(tks.get("to",0))
        if xfrom> xto:
            _to = xto
            xto = xfrom
            xfrom = _to
        return {"type":"Year".upper(), "xfrom":xfrom, "xto":xto  }
    @staticmethod
    def parse_year(tks:ParserElement):
        value = tks.get("value",0)
        # print("VALUE", value)
        val = int(value)
        return {"type":"Year".upper(), "xfrom":val, "xto":val}
    @staticmethod
    def parse_element(tks:ParserElement):
        if "years" in tks:
            years = tks.get("years")
            return years
        elif "year" in tks:
            year = tks.get("year")
            return year
        # return {"type": , "values": tks.get("values", []).asList() }

class SpatialVariableParseActions:
    def parse(tks):
        elements = tks.get("element").as_list()
        variable_type = tks.get("variable_type")
   
        return {
            "variable_type":variable_type,
            "elements":elements
        }

    def parse_elements(tks):
        elems = tks.asList()
        v_len = len(elems)
        if v_len == 1:
            if elems[0]=="*":
                return [{"type":"WILDCARD", "value":"*"}]
        return tks

    def parse_sequence(tks):
        sequence = tks.asList()
        h        = H.sha256()
        if len(sequence) == 1:
            return sequence[0]
        for v in sequence:
            h.update(v.get("xvid").encode())
        return {
            "type":"SEQUENCE",
            "values":sequence,
            "xvid":h.hexdigest()
        }

    def parse_element(tks):
        _type = tks.get("type","TYPE").upper()
        value = tks.get("value","VALUE").upper()
        xvid_str  = f"{_type}{value}"
        h = H.sha256()
        h.update(xvid_str.encode())
        return {
            "type":_type,
            "value":value,
            "xtype":"STRING",
            "xvid":h.hexdigest()
        }