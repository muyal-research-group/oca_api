from pyparsing import Word, alphas, alphanums, nums, Literal, delimitedList,OneOrMore,MatchFirst,Combine,Optional,CaselessLiteral,ZeroOrMore,ParserElement
from ocaapi.dto.v2 import XVariableDTO
from ocaapi.models.v2 import XType,XVariableType
import json as J
from ocaapi.querylang.parser import TemporalVariableParseActions
from datetime import datetime
import calendar

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
        keys = list(tks.keys())
        return tks.get("values",[])
    
    @staticmethod
    def parse_value(tks):
        return tks
    @staticmethod
    def parse_tv_day(tks):
        return tks
    
    @staticmethod
    def parse_tv_year(tks):
        return tks
    @staticmethod
    def parse_range_value(tks):
        keys = list(tks.keys())
        # print("KEYS",keys)
        if "int_month" in keys:
            month_int = int(tks.get("int_month","1"))
            month_int = 1 if month_int == 0 else month_int
            month_str = TemporalVariableParseActions.INT_TO_STR_MONTH[month_int]
        elif "str_month" in keys:
            month_str = tks.get("str_month","JAN").upper()
            month_int = TemporalVariableParseActions.MONTH_TO_INT[month_str.lower()]
        # print(list(tks.keys()))
        year = int(tks.get("year"))
        day = int(tks.get("day"))
        value = datetime(year=year,month=month_int, day=day)
        _type = tks.get("type").upper()
        xvar = XVariableDTO(type=_type,xtype=XType.Date, variable_type=XVariableType.Temporal, value=value)
        return xvar
    
    @staticmethod
    def parse_tv_month(tks):
        return tks

    @staticmethod
    def parse_tv_element(tks):
        keys = list(tks.keys())
        if "int_month" in keys:
            month_int = int(tks.get("int_month","1"))
            month_int = 1 if month_int == 0 else month_int
            month_str = TemporalVariableParseActions.INT_TO_STR_MONTH[month_int]
        elif "str_month" in keys:
            month_str = tks.get("str_month","JAN").upper()
            month_int = TemporalVariableParseActions.MONTH_TO_INT[month_str.lower()]
        # print(list(tks.keys()))
        year = int(tks.get("year"))
        day = int(tks.get("day"))
        value = datetime(year=year,month=month_int, day=day)
        _type = tks.get("type").upper()
        xvar = XVariableDTO(type=_type,xtype=XType.Date, variable_type=XVariableType.Temporal, value=value)
        return xvar
    
    @staticmethod
    def parse_tv_range(tks):
        keys       = list(tks.keys())
        a          = tks.get("a")
        b          = tks.get("b")
        right_open = "ropen" in keys
        left_open  = "lopen" in keys

        return XVariableDTO(
            type="DateRange".upper(),
            value={
                "left_open":left_open,
                "right_open":right_open,
                "start":a.value,
                "end":b.value,
            },
            variable_type=XVariableType.Temporal,
            xtype=XType.DateRange,
        )

    @staticmethod
    def parse_year(tks):
        keys = list(tks.keys())
        year = int(tks.get("year"))
        return XVariableDTO(
            value = year,
            type  = "YEAR",
            xtype= XType.Integer,
            variable_type=XVariableType.Temporal,
        )
    
    @staticmethod
    def parse_years_range(tks):
        keys = list(tks.keys())
        # print("KEYS",keys)
        a = tks.get("a")
        b = tks.get("b")
        right_open = "ropen" in keys
        left_open  = "lopen" in keys
        # print("A",a)
        # # print("B",b)
        return XVariableDTO(
            type="Range",
            xtype=XType.IntegerRange,
            value= {
                "step":1,
                "start":a.value,
                "end":b.value,
                "right_open":right_open,
                "left_open":left_open
            },
            variable_type=XVariableType.Temporal
        )
    @staticmethod
    def parse_range(tks):
        keys = list(tks.keys())
        a    = int(tks.get("a"))
        b    = int(tks.get("b"))
        step = int(tks.get("step",1))
        return XVariableDTO(
            type="Range", 
            xtype=XType.IntegerRange,
            value={
                "step":step,
                "start":a,
                "end":b,
                "right_open":False,
                "left_open":False
            },
            variable_type=XVariableType.Temporal
        )

    




# Define atomic components
identifier = Word(alphanums, alphanums + "_" +"-")
word_with_spaces = Word(alphas + " ")  # Allows space in words like "Pedro Antonio Santos"

number     = Word(nums)
# Pattern to allow either comma or dot as a decimal separator
floating_number = Combine(
    number +
    Optional(
        ('.' + number)
    )
)
# ____________________________________________
wildcard           = Literal('*')
less_than          = Literal("<").setResultsName("lt")
less_equal_than    = Literal("=<").setResultsName("leq")
greater_equal_than = Literal(">=").setResultsName("geq")
greater_than       = Literal(">").setResultsName("gt")
equal_to           = Literal("==").setResultsName("eq")
arrow              = Literal("->").suppress()
equals             = Literal("=").suppress()
lparen             = Literal("(").suppress()
rparen             = Literal(")").suppress()
lsquareb           = Literal("[").suppress()
rsquareb           = Literal("]").suppress()
comma              = Literal(",").suppress()
dot                = Literal(".").suppress()

tv_str_months = (
    CaselessLiteral("january") | CaselessLiteral("jan") |
    CaselessLiteral("february") | CaselessLiteral("feb") |
    CaselessLiteral("march") | CaselessLiteral("mar") |
    CaselessLiteral("april") | CaselessLiteral("apr") |
    CaselessLiteral("may") |
    CaselessLiteral("june") | CaselessLiteral("jun") |
    CaselessLiteral("july") | CaselessLiteral("jul") |
    CaselessLiteral("august") | CaselessLiteral("aug") |
    CaselessLiteral("september") | CaselessLiteral("sep") | CaselessLiteral("sept") |
    CaselessLiteral("october") | CaselessLiteral("oct") |
    CaselessLiteral("november") | CaselessLiteral("nov") |
    CaselessLiteral("december") | CaselessLiteral("dec")
)
tv_date_month = (number.setResultsName("int_month") | tv_str_months.setResultsName("str_month")).setResultsName("month").setParseAction(TemporalVariableParseActions.parse_tv_month)
tv_date_day   = (number).setResultsName("day").setParseAction(TemporalVariableParseActions.parse_tv_day)
tv_date_year  = (number).setResultsName("year").setParseAction(TemporalVariableParseActions.parse_tv_year)

tv_element     = (Literal("Date").setResultsName("type") + lparen +( tv_date_month+ comma +tv_date_day +comma+ tv_date_year )+ rparen).setParseAction(TemporalVariableParseActions.parse_tv_element)

tv_range_value = (Literal("Date").setResultsName("type")+lparen+ tv_date_month+ comma +tv_date_day +comma+ tv_date_year +rparen)


left_open   = Literal("(").setResultsName("lopen")
left_closed = Literal("[").setResultsName("lclosed")
left_limits = ( left_open| left_closed )

right_open = Literal(")").setResultsName("ropen")
right_closed = Literal("]").setResultsName("rclosed")
right_limits = ( right_open | right_closed)

tv_date_range   = ( left_limits+ tv_range_value.setResultsName("a").setParseAction(TemporalVariableParseActions.parse_range_value) +comma+ tv_range_value.setResultsName("b").setParseAction(TemporalVariableParseActions.parse_range_value) + right_limits ).setParseAction(TemporalVariableParseActions.parse_tv_range)

tv_year = (Literal("Year") + lparen+number.setResultsName("year") +rparen ).setParseAction(TemporalVariableParseActions.parse_year)
tv_years_range = (left_limits+ tv_year.setResultsName("a") + comma + tv_year.setResultsName("b")  + right_limits).setParseAction(TemporalVariableParseActions.parse_years_range)


tv_range = (Literal("Range") +lparen+number.setResultsName("a")+comma+number.setResultsName("b")+comma+number.setResultsName("step")+rparen ).setParseAction(TemporalVariableParseActions.parse_range)
# .setParseAction(TemporalVariableParseActions.parse_years_range)

tv_value = (wildcard | tv_range |tv_year|tv_years_range|  tv_date_range | tv_element ).setResultsName("value")\
    .setParseAction(TemporalVariableParseActions.parse_value)

tv       = (
    Literal("TV").setResultsName("variable_type") + equals + delimitedList(tv_value).setResultsName("values")) \
    .setResultsName("tv").setParseAction(TemporalVariableParseActions.parse) 
