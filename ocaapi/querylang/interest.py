from pyparsing import Word, alphas, alphanums, nums, Literal, delimitedList,OneOrMore,MatchFirst,Combine,Optional,CaselessLiteral,ZeroOrMore
from ocaapi.dto.v2 import XVariableDTO
from ocaapi.models.v2 import XType,XVariableType
import json as J

class InterestVariableParseActions:
    def parse_element(tks):
        _type = tks.get("type")
        value = tks.get("value").asList()
        xs = []
        # if isinstance(value, list):
        for v in value:
            x = XVariableDTO(
                type          = _type.upper(),
                xtype         = XType.String,
                variable_type = XVariableType.Interest,
                value         = v.upper()
            )
            xs.append(x)
        return xs
    
    def parse_iv_hierarchy_element(tks):
        return tks

    def parse_iv_hierarchy(tks):
        return tks

    def parse_iv_ranges(tks):
        return tks
    
    def parse_value(tks):
        return tks
    
    def parse(tks):
        keys = list(tks.keys())
        print("PARSE_ELEMENT",keys)
        return tks.get("values",[])

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

iv_element = (
    identifier.setResultsName("type") + lparen + delimitedList(word_with_spaces | identifier).setResultsName("value") + rparen
).setParseAction(InterestVariableParseActions.parse_element)

iv_hierarchy_element = (identifier.setResultsName("type" ) + lparen + (floating_number|word_with_spaces | identifier | "").setResultsName("value") + rparen).setResultsName("val").setParseAction(InterestVariableParseActions.parse_iv_hierarchy_element)
iv_hierarchy         = (iv_hierarchy_element + OneOrMore(arrow + iv_hierarchy_element)).setParseAction(InterestVariableParseActions.parse_iv_hierarchy)


iv_ranges   = (identifier.setResultsName("type") + lparen  + ((Literal("(").setResultsName("lopen") | Literal("[").setResultsName("lclosed") ) + floating_number.setResultsName("a") + comma + floating_number.setResultsName("b") + (Literal(")").setResultsName("ropen") | Literal("]").setResultsName("rclosed") )) + rparen ).setParseAction(InterestVariableParseActions.parse_iv_ranges)
iv_elements = delimitedList(iv_hierarchy | iv_ranges | iv_element  )
iv_value    = (wildcard | iv_elements)
# .setParseAction(InterestVariableParseActions.parse_value)
iv          = (Literal("IV").setResultsName("variable_type") + equals + iv_value.setResultsName("values") ).setParseAction(InterestVariableParseActions.parse).setResultsName("iv")
