import ply.yacc as yacc
import ply.lex as lex
import jstokens                 # use our JavaScript lexer
from jstokens import tokens     # use our JavaScript tokens

start = 'exp'    # we'll start at expression this time

precedence = (
        # Fill in the precedence and associativity. List the operators
        # in order of _increasing_ precedence (start low, go to high). 
    ('left', 'OROR'),
    ('left', 'ANDAND'),
    ('left', 'EQUALEQUAL'),
    ('left', 'LT', 'LE', 'GT', 'GE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MOD'),
    ('right', 'NOT'),    
) 

# Here's the rules for simple expressions.
def p_exp_identifier(p):
    
    'exp : IDENTIFIER'
    p[0] = ("identifier",p[1]) 
        
def p_exp_number(p):
    
    'exp : NUMBER'
    p[0] = ('number',p[1])

def p_exp_string(p):
    
    'exp : STRING'
    p[0] = ('string',p[1])
    
def p_exp_true(p):
    
    'exp : TRUE'
    p[0] = ('true','true')
    
def p_exp_false(p):
    
    'exp : FALSE'
    p[0] = ('false','false')
    
def p_exp_not(p):
    
    'exp : NOT exp'
    p[0] = ('not', p[2])
    
def p_exp_parens(p):
    
    'exp : LPAREN exp RPAREN'
    p[0] = p[2]

# This is what the rule for anonymous functions would look like, but since
# they involve statements they are not part of this assignment. Leave this
# commented out, but feel free to use it as a hint.
#
## def p_exp_lambda(p):
##         'exp : FUNCTION LPAREN optparams RPAREN compoundstmt'  
##         p[0] = ("function",p[3],p[5])


def p_exp_binop(p):
    
    '''exp : exp PLUS exp
             | exp MINUS exp
             | exp TIMES exp
             | exp MOD exp
             | exp DIVIDE exp
             | exp EQUALEQUAL exp
             | exp LE exp
             | exp LT exp
             | exp GE exp
             | exp GT exp
             | exp ANDAND exp
             | exp OROR exp'''
    
    p[0] = ("binop", p[1], p[2], p[3])

def p_exp_call(p):
    
    'exp : IDENTIFIER LPAREN optargs RPAREN'
    p[0] = ("call", p[1], p[3])

def p_optargs(p):
    
    'optargs : args'
    p[0] = p[1]

def p_optargs_empty(p):
    
    'optargs : '
    p[0] = []

def p_args(p):
    
    'args : exp COMMA args'
    p[0] = [p[1]] + p[3]

def p_args_one(p):
    
    'args : exp'
    p[0] = [p[1]]


jslexer = lex.lex(module=jstokens) 
jsparser = yacc.yacc() 

def test_parser(input_string):  # invokes your parser to get a tree!
        jslexer.input(input_string) 
        parse_tree = jsparser.parse(input_string,lexer=jslexer) 
        return parse_tree

# Simple binary expression.
jstext1 = "x + 1" 
jstree1 = ('binop', ('identifier', 'x'), '+', ('number', 1.0))
print (test_parser(jstext1) == jstree1)

# Simple associativity.
jstext2 = "1 - 2 - 3"   # means (1-2)-3
jstree2 = ('binop', ('binop', ('number', 1.0), '-', ('number', 2.0)), '-',
('number', 3.0))
print (test_parser(jstext2) == jstree2)

# Precedence and associativity.
jstext3 = "1 + 2 * 3 - 4 / 5 * (6 + 2)" 
jstree3 = ('binop', ('binop', ('number', 1.0), '+', ('binop', ('number', 2.0), '*', ('number', 3.0))), '-', ('binop', ('binop', ('number', 4.0), '/', ('number', 5.0)), '*', ('binop', ('number', 6.0), '+', ('number', 2.0))))
print (test_parser(jstext3) == jstree3)

# String and boolean constants, comparisons.
jstext4 = ' "hello" == "goodbye" || true && false '
jstree4 = ('binop', ('binop', ('string', 'hello'), '==', ('string', 'goodbye')), '||', ('binop', ('true', 'true'), '&&', ('false', 'true')))
print (test_parser(jstext4) == jstree4)

# Not, precedence, associativity.
jstext5 = "! ! tricky || 3 < 5" 
jstree5 = ('binop', ('not', ('not', ('identifier', 'tricky'))), '||', ('binop', ('number', 3.0), '<', ('number', 5.0)))
print (test_parser(jstext5) == jstree5)

# nested function calls!
jstext6 = "apply(1, 2 + eval(recursion), sqrt(2))"
jstree6 = ('call', 'apply', [('number', 1.0), ('binop', ('number', 2.0), '+', ('call', 'eval', [('identifier', 'recursion')])), ('call', 'sqrt', [('number', 2.0)])])
print (test_parser(jstext6))
