from pyparsing import Word, alphas, alphanums, nums, oneOf, Literal, Group, delimitedList, Suppress, Forward,OneOrMore,MatchFirst,Dict,Combine,Optional,CaselessLiteral
import json as J
from ocaapi.querylang.parser import ProductTypeParseActions,InterestVariableParseActions,TemporalVariableParseActions,SpatialVariableParseActions,ObservableParseActions,InfoParseActions


# Define atomic components
identifier = Word(alphas, alphanums + "_" +"-")
word_with_spaces = Word(alphas + " ")  # Allows space in words like "Pedro Antonio Santos"

number     = Word(nums)
# Pattern to allow either comma or dot as a decimal separator
floating_number = Combine(
    number +
    Optional(
        ('.' + number) | (',' + number)
    )
)

wildcard           = Literal('*')
less_than          = Literal("<").setResultsName("lt")
less_equal_than    = Literal("=<").setResultsName("leq")
greater_equal_than = Literal(">=").setResultsName("geq")
greater_than       = Literal(">").setResultsName("gt")
equal_to           = Literal("==").setResultsName("eq")
arrow              = Literal("->").suppress()
equals             = Literal("=").suppress()
lparen             = Literal("(").suppress()
rparen     = Literal(")").suppress()
comma = Literal(",").suppress()
dot   = Literal(".").suppress()
# ____________________________________________
sv_element = (
    identifier.setResultsName("type") + lparen+(word_with_spaces | identifier).setResultsName("value") +rparen
).setParseAction(SpatialVariableParseActions.parse_element)
sv_sequence = (
    sv_element + OneOrMore(arrow + sv_element)
).setParseAction(SpatialVariableParseActions.parse_sequence)
sv_value = (wildcard | delimitedList(sv_sequence | sv_element)).setResultsName("element").setParseAction(SpatialVariableParseActions.parse_elements)
sv       = (
    Literal("SV").setResultsName("variable_type") + 
    equals + 
    sv_value
).setParseAction(SpatialVariableParseActions.parse).setResultsName("sv")
# ____________________________________________
year             = "Year"
years            = "Years"
num_word         = Word(nums +" ")
tv_years_element = (years + lparen + (num_word.setResultsName("from") + comma + num_word.setResultsName("to") ) + rparen ).setParseAction(TemporalVariableParseActions.parse_years)
tv_year_element  = (year + lparen + num_word.setResultsName("value")+rparen).setParseAction(TemporalVariableParseActions.parse_year)
tv_element       = (
    tv_years_element.setResultsName("years")  | delimitedList(tv_year_element).setResultsName("year")
).setParseAction(TemporalVariableParseActions.parse_element)
tv_value = (wildcard | tv_element).setResultsName("value").setParseAction(TemporalVariableParseActions.parse_value)
tv       = (Literal("TV").setResultsName("variable_type") + equals + tv_value).setParseAction(TemporalVariableParseActions.parse).setResultsName("tv")
# ____________________________________________
iv_element = (
    identifier.setResultsName("type") + lparen + delimitedList(word_with_spaces | identifier).setResultsName("value") + rparen
).setParseAction(InterestVariableParseActions.parse_element)
iv_elements = delimitedList(iv_element)
iv_value    = MatchFirst([wildcard, iv_elements]).setResultsName("value").setParseAction(InterestVariableParseActions.parse_value)
iv          = (Literal("IV").setResultsName("variable_type") + equals + iv_value ).setParseAction(InterestVariableParseActions.parse).setResultsName("iv")
# ____________________________________________
pt_elements = delimitedList(identifier)
pt_value    = MatchFirst([wildcard,pt_elements]).setResultsName("value").setParseAction(ProductTypeParseActions.parse_value)
pt          = (Literal("ProductType").setResultsName("variable_type")  + equals + pt_value).setParseAction(ProductTypeParseActions.parse).setResultsName("pt")
# ____________________________________________
ov_elements = (floating_number | identifier)
ov_value    = MatchFirst([wildcard, ov_elements]).setResultsName("value").setParseAction(ObservableParseActions.parse_value)
ov          = (Literal("OV").setResultsName("variable_type") + equals + ov_value).setParseAction(ObservableParseActions.parse).setResultsName("ov")
# ____________________________________________
average_id = (CaselessLiteral("Average") | CaselessLiteral("Avg") | CaselessLiteral("Mean") ).setResultsName("stat_name")
# average    = ( average_id + lparen + floating_number.setResultsName("stat_value") + rparen)
# _____________________________________________
median_id  = (CaselessLiteral("Median") ).setResultsName("stat_name")
# median       = (median_id + lparen + floating_number.setResultsName("stat_value") + rparen)
# _____________________________________________
std_id       = (CaselessLiteral("Std") | CaselessLiteral("StandardDeviation") ).setResultsName("stat_name")
# std          = ( std_id + lparen + floating_number.setResultsName("stat_value") + rparen)
# _____________________________________________
mode_id      = (CaselessLiteral("Mode")  ).setResultsName("stat_name")
# mode         = (mode_id + lparen + floating_number.setResultsName("stat_value") + rparen)
# _____________________________________________
variance_id  = (CaselessLiteral("Variance")  ).setResultsName("stat_name")
# variance     = (variance_id + lparen + floating_number.setResultsName("stat_value") + rparen)
# _____________________________________________
quartile_id  = (CaselessLiteral("Q1") | CaselessLiteral("Q2") | CaselessLiteral("Q3")  ).setResultsName("stat_name") 
#  -> IQR
#  -> Min, Max
#  -> Upper and lower bound
#  -> ConfidenceInterval 
# quartile     = ( quartile_id+ lparen + floating_number.setResultsName("stat_value") + rparen)

stats_ids    = (average_id | median_id | std_id | mode_id | variance_id | quartile_id )

stats        = (stats_ids  +lparen + floating_number.setResultsName("stat_value") + rparen ).setResultsName("stat").setParseAction(InfoParseActions.parse_stats)
# (average  | median | std | mode | variance | quartile ).setResultsName("stat").setParseAction(InfoParseActions.parse_stats)

info_iv      = (identifier.setResultsName("iv_type") + lparen + delimitedList(word_with_spaces | identifier).setResultsName("iv_value") + rparen)

info_element = (identifier.setResultsName("ov")+ dot + info_iv +dot+stats ).setParseAction(InfoParseActions.parse_info_element)

# info_elements = 
# info_value = delimitedList(identifier).setResultsName("value")
info_value = (delimitedList(info_element)).setResultsName("value").setParseAction(InfoParseActions.parse_value)

info = (Literal("Info").setResultsName("variable_type") + equals + info_value).setResultsName("info").setParseAction(InfoParseActions.parse)

inequality_symbols = (less_than | less_equal_than | greater_than | greater_equal_than | equal_to)
info_query_left    = (identifier.setResultsName("ov") + dot + info_iv)
info_query_right   = ( (stats_ids + lparen+ (  info_query_left) +rparen) | floating_number) 
info_query_value   = ( info_query_left.setResultsName("left").setParseAction(InfoParseActions.parse_info_query_left) +  inequality_symbols + info_query_right.setResultsName("right") )
# .setParseAction(InfoParseActions.parse_info_query_value)
info_query         = (Literal("Info").setResultsName("variable_type") + equals + info_query_value).setParseAction(InfoParseActions.parse_info_query)



def grammar_parse_action(tks):
    return tks

grammar = OneOrMore(sv | tv | iv | ov | pt).setParseAction(grammar_parse_action)
# .setParseAction(grammar_parse_action)

# Parse each line from the input (assuming multi-line input)
# input_text = """
# SV = Country(MEXIco)->StaTE(San LUis Potosi)
# TV = Years(2000,2020)
# IV = Sex(Male), Sex(Female)
# OV = RateLimit100k
# ProductType = Map, BarPlot
# """

def parse_sv(x:str):
    return sv.parseString(x)
def parse_tv(x:str):
    return tv.parseString(x)
def parse_iv(x:str):
    return iv.parseString(x)
def parse_pt(x:str):
    return pt.parseString(x)
def parse_ov(x:str):
    return ov.parseString(x)

def parse(x:str):
    return grammar.parseString(x)


# def parse(x:str)
# result = grammar.parseString(input_text)
# print(result.as_dict())
# print(list(result.keys()))
# print(J.dumps(result.asDict(), indent=4))



# from pydantic import BaseModel
# from typing import List
