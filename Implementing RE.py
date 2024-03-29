import ply.lex as lex
import ply.yacc as yacc

# Fill in your code here. 

tokens = ('BAR', 'STAR', 'LPAREN', 'RPAREN', 'LETTER')
t_BAR = r'\|'
t_STAR = r'\*'
t_LPAREN = r'\('
t_RPAREN = r'\)'

# token rules

def t_LETTER(t):
    
    r"[A-Za-z0-9]"
    
    return t
    
t_ignore = ' \t\v\r'

def t_error(t):
    
    print ("Lexer: unexpected character " + t.value[0])
    
    t.lexer.skip(1)

# precedence ordering
start = 're'

precedence = (
    ('left', 'BAR'),
    ('left', 'CONCAT'),
    ('left', 'STAR'),
)

def p_re_letter(p):
    
    "re : LETTER %prec CONCAT"
    p[0] = ("letter", p[1])

def p_re_concat(p):
    
    "re : re re %prec CONCAT"
    p[0] = ("concat", p[1], p[2])

def p_re_bar(p):
    
    "re : re BAR re"
    p[0] = ("bar", p[1], p[3])

def p_re_star(p):
    
    "re : re STAR"
    p[0] = ("star", p[1])

def p_re_paren(p):
    
    "re : LPAREN re RPAREN"
    p[0] = p[2]

def p_error(p):
    
    raise SyntaxError

state_counter = 3

lexer = lex.lex()
parser = yacc.yacc()

def interpret(ast):
    
    global state_counter
    
    start_state = 1
    
    accepting = [2]
    
    state_counter = 3
    
    edges = {}
    
    def add_edge(a, b, l): # helper function to add edges
    
        if (a, l) in edges:
            
            edges[(a, l)] = [b] + edges[(a, 1)]
            
        else:
            
            edges[(a, l)] = [b]
            
    def new_state(): # helper function to add a new state
    
        global state_counter
        
        x = state_counter
        
        state_counter = state_counter + 1
        
        return x
        
    def walk(re, here, goal): # helper function to walk the ast
    
        retype = re[0]
        
        if retype == "letter": # see a plain letter, that's a transition we have to take
        
            add_edge(here, goal, re[1])
            
        elif retype == "concat": # see concat then we have to take both, in order
        
            mid = new_state()
            
            walk(re[1], here, mid)
            
            walk(re[2], mid, goal)
            
        elif retype == "bar": # a bar means we go from the current state to two different states
        
            walk(re[1], here, goal)
            
            walk(re[2], here, goal)
            
        elif retype == "star": # and a star will have a loop back to the current state
        
            walk(re[1], here, here)
            
            add_edge(here, goal, None)
            
        else:
            
            print ("OOPS" + re)
            
    walk(ast, start_state, accepting[0])
    
    return (edges, accepting, start_state)

def re_to_nfsm(re_string): 
    
        lexer.input(re_string)
        
        parse_tree = parser.parse(re_string, lexer=lexer) 
        
        return interpret(parse_tree) 

def nfsmaccepts(edges, accepting, current, string, visited): 
    
        # If we have visited this state before, return false. 
        if (current, string) in visited:
            
                return False
                
        visited.append((current, string))       

        # Check all outgoing epsilon transitions (letter == None) from this state. 
        if (current, None) in edges:
            
                for dest in edges[(current, None)]:
                    
                        if nfsmaccepts(edges, accepting, dest, string, visited):
                            
                                return True

        # If we are out of input characters, check if this is an accepting state. 
        if string == "":
            
                return current in accepting

        # If we are not out of input characters, try all possible outgoing transitions labeled with the next character. 
        letter = string[0]
        
        rest = string[1:]
        
        if (current, letter) in edges:
            
                for dest in edges[(current, letter)]:
                    
                        if nfsmaccepts(edges, accepting, dest, rest, visited):
                            
                                return True
                                
        return False

def test(re_string, e, ac_s, st_s, strings):
    
  my_e, my_ac_s, my_st_s = re_to_nfsm(re_string) 
  
  print (my_e)
  
  for string in strings:
      
      print (nfsmaccepts(e,ac_s,st_s,string,[]) == nfsmaccepts(my_e,my_ac_s,my_st_s,string,[])) 

edges = { (1,'a')  : [ 2 ] ,
          (2,None) : [ 3 ] ,    # epsilon transition
          (2,'b')  : [ 2 ] ,
          (3,'c')  : [ 4 ] } 
          
accepting_state = [4]

start_state = 1

test("a(b*)c", edges, accepting_state, start_state, 
  [ "", "ab", "cd", "cddd", "c", "", "ad", "abcd", "abbbbbc", "ac" ]  ) 

edges = { (1,'a')  : [ 2 ] ,
          (2,'b') :  [ 1 ] ,    
          (1,'c')  : [ 3 ] ,
          (3,'d')  : [ 1 ] } 
          
accepting_state = [1]

start_state = 1

test("((ab)|(cd))*", edges, accepting_state, start_state, 
  [ "", "ab", "cd", "cddd", "c", "", "ad", "abcd", "abbbbbc", "ac" ]  ) 
