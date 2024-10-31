from pyparsing import ParserElement,ParseResults
from typing import Set,Dict,Any


class InfoParseActions:

    def parse(tks:ParserElement):
        print(list(tks.keys()))
        val = tks.get("value")
        # print("PASE_VALUE",val.asList())
        return {
            "variable_type":tks.get("variable_type","UKNOWN"),
            "value":val.asList()
        }

    def parse_value(tks:ParserElement):
        return tks

    def parse_stats(tks:ParserElement):
        name = tks.get("stat_name","UKNOWN")
        val  = tks.get("stat_value","0")
        return {"type":name, "value":float(val)}

    def parse_info_element(tks:ParserElement):
        ov      = tks.get("ov")
        iv_type = tks.get("iv_type")
        iv_val  = tks.get("iv_value")
        stat    = tks.get("stat")
        return {"ov":ov, "iv_type":iv_type, "iv_value":iv_val[0],"stat":stat.get("type"),"value":stat.get("value") }

    def parse_info_query(tks:ParserElement):
        print("PASRSE_INFO_QUERY", tks )
        return tks
    def parse_info_query_value(tks:ParserElement):
        print("PARSEa_INFO_QUERY_VALUE",list(tks.keys()))
        left       = tks.get("left")
        right      = tks.get("right")
        print("LEFT",list(left.keys()))
        print(dir(left),list(left.values()))
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
        return tks

class ObservableParseActions:

    @staticmethod
    def parse_value(tks:ParserElement):
        values = tks.asList()
        elements = []
        print("VALUE",values)
        for value in values:
            if type(value) == str:
                elements.append({"type":"Metric".upper(), "value":value.upper()})
            else:
                val = float(value)
                elements.append({"type":"MetricValue".upper(), "value":val})
        return elements

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
        print("TKS",elements)
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
            elements.append({"type":"ProductType".upper(), "value":v.upper()})
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
    def parse_element(tks:ParserElement):
        value = tks.get("value","VALUE").asList()
        return { "type": tks.get("type","TYPE").upper(), "value":value }

    @staticmethod
    def parse_value(tks:ParserElement):
        vs = tks.get("value",[])
        v_len = len(vs)
        if v_len ==1:
            if vs[0] =="*":
                return [{"type":"WILDCARD", "value":"*"}]
        map_type:Dict[str, Set] = {}
        for value in vs:
            type_ = value.get("type","UKNOWN")
            value = value.get("value",[])
            if len(value) ==0:
                continue
            current_values = map_type.setdefault(type_,set())
            values = set(value)
            map_type[type_] = current_values.union(values)
        result = []
        for k,vss in map_type.items():
            for vx in vss:
                result.append({"type":k.upper(), "value":vx.upper()})
        return result

class TemporalVariableParseActions:
    @staticmethod
    def parse(tks):
        return {"variable_type":tks.get("variable_type","UKNOWN_VARIABLE") , "elements": tks.get("value",[]).asList() }
    @staticmethod
    def parse_value(tks:ParserElement):
        value = tks.get("value",[])
        v_len = len(value)
        print("TEM<PORAL", value)
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
        # xs = tks.asList()
        elements = tks.get("element").as_list()
        variable_type = tks.get("variable_type")
        # print("ELENMTS", elements)
        filtered = [[e] if type(e) is dict else e   for e in elements]
        # filtered = []
        # for e in elements:
            # print(e, type(e) is dict)
        return {
            "variable_type":variable_type,
            "elements":filtered
        }

    def parse_elements(tks):
        elems = tks.asList()
        v_len = len(elems)
        if v_len == 1:
            if elems[0]=="*":
                return [{"type":"WILDCARD", "value":"*"}]
        # print("ELEMENTs", elems)
        return tks

    def parse_sequence(tks):
        sequence = tks.asList()
        return [sequence]
        # return {"sequence": sequence}

    def parse_element(tks):
        return {"type":tks.get("type","TYPE").upper(),"value":tks.get("value","VALUE").upper()}