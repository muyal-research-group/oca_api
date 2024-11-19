from pyparsing import Word, alphas, alphanums, nums, Literal, delimitedList,OneOrMore,MatchFirst,Combine,Optional,CaselessLiteral,ZeroOrMore,ParserElement
from ocaapi.dto.v2 import XVariableDTO
from ocaapi.models.v2 import XVariableType,XType

identifier = Word(alphanums, alphanums + "_" +"-")
word_with_spaces = Word(alphas + " ")  # Allows space in words like "Pedro Antonio Santos"

number     = Word(nums)
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

# ____________________________________________
class SpatialVariableParseActions:

    @staticmethod
    def parse(tks):
        value =tks.get("value",[])
        return value
    
    @staticmethod
    def parse_element(tks:ParserElement):
        _type = tks.get("type","")
        value = tks.get("value","")
        dto   = XVariableDTO(type=_type, value=value,xtype=XType.String,variable_type=XVariableType.Spatial)
        return dto

    @staticmethod
    def parse_sequence(tks:ParserElement):
        return [tks]

    @staticmethod
    def parse_elements(tks:ParserElement):
        # print("ELEMENTS",tks)
        # print("*"*40)
        return tks

# ____________________________________________
sv_element = (
    identifier.setResultsName("type") + lparen+(word_with_spaces | identifier).setResultsName("value") +rparen
).setParseAction(SpatialVariableParseActions.parse_element)


sv_hierarchy = (
    sv_element + ZeroOrMore(arrow + sv_element)
).setParseAction(SpatialVariableParseActions.parse_sequence)

sv_value = (wildcard | delimitedList(sv_hierarchy)).setResultsName("value").setParseAction(SpatialVariableParseActions.parse_elements)

sv       = (
    Literal("SV").setResultsName("variable_type") + 
    equals + 
    sv_value
).setParseAction(SpatialVariableParseActions.parse).setResultsName("sv")