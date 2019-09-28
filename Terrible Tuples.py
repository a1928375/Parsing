import ply.lex as lex
import ply.yacc as yacc

start = 'exp'    # the start symbol in our grammar

def p_exp(p):
    
    "exp : NUMBER"
    p[0] = ("number", p[1])
    
def p_exp_tuple(p):
    
    "exp : LPAREN expcomma RPAREN"
    if len(p[2]) == 1:
        
        p[0] = p[2][0]
    
    else:
        
        p[0] = ("tuple", p[2])
    
def p_expcomma(p):
    
    "expcomma : exp COMMA expcomma"
    p[0] = [p[1]]+p[3]

def p_expcomma_none(p):
    
    "expcomma : exp"
    p[0] = [p[1]]

def p_exp_list(p):
    
    "exp : LBRACKET expcomma RBRACKET"
    p[0] = ("list", p[2])


def p_error(p):

        raise SyntaxError

tokens = ('LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET', 'NUMBER', 'COMMA') 

def t_NUMBER(token):
    
        r"[0-9]+"
        token.value = int(token.value)
        
        return token

t_ignore        = ' \t\v\r'
t_COMMA         = r','
t_LPAREN        = r'\(' 
t_RPAREN        = r'\)' 
t_LBRACKET      = r'\[' 
t_RBRACKET      = r'\]' 

def t_error(t):
    
  print ("Lexer: unexpected character " + t.value[0])
  t.lexer.skip(1) 

lexer = lex.lex() 

def test(input_string):
    
  lexer.input(input_string)
  parser = yacc.yacc()
  
  try:
      
    parse_tree = parser.parse(input_string, lexer=lexer)
    
    return parse_tree

  except:
      
    return "error" 

question1 = " 123 " 
answer1 = ('number', 123)
print (test(question1) == answer1)

question2 = " (123) " 
print (test(question2) == answer1)

question3 = " (1,2,3) " 
answer3 = ('tuple', [('number', 1), ('number', 2), ('number', 3)])
print (test(question3) == answer3)

question4 = " [123] " 
answer4 = ('list', [('number', 123)])
print (test(question4) == answer4)

question5 = " [1,2,3] " 
answer5 = ('list', [('number', 1), ('number', 2), ('number', 3)])
print (test(question5) == answer5)

question6 = " [(1,2),[3,[4]]] "
answer6 = ('list', [('tuple', [('number', 1), ('number', 2)]), ('list', [('number', 3), ('list', [('number', 4)])])])
print (test(question6) == answer6) 

question7 = " (1,2) [3,4) " 
answer7 = "error"
print (test(question7) == answer7)
