# Parsing

(1) Optional Arguments: 

JavaScript allows function calls:
    
    myfun(11,12)
    'exp : IDENTIFIER LPAREN optargs RPAREN'

We want the parse tree to be:  ("call", "myfun", [("number", 11), ("number", 12)]).

(2) Parsing Javascript Statements:  In this exercise you will write a Parser for a subset of JavaScript. This will invole writing parsing rewrite rules (i.e., encoding a context-free grammar) and building up a parse tree (also called a syntax tree) of the result.  We have split the parsing of JavaScript into two exercises so that you have a chance to demonstrate your mastery of the concepts independently (i.e., so that you can get one of them right even if the other proves difficult). We could easily make a full JavaScript parser by putting all of the rules together. In the first part, we will handle JavaScript elements and statements. The JavaScript tokens we use will be the same ones we defined together in the Homework for Unit 2. (Even if you did not complete Homework 2, the correct tokens will be provided here.) Let's walk through our JavaScript grammar. We'll describe it somewhat informally in text: your job for this homework problem is to translate this description into a valid parser! The starting non-terminal is "js" for "JavaScript program" -- which is just a list of "elements" (to be defined shortly). The parse tree you must return is simply a list containing all of the elements.  

        js -> element js
        js -> 

An element is either a function declaration: 

        element -> FUNCTION IDENTIFIER ( optparams ) compoundstmt

or a statement following by a semi-colon: 

        element -> stmt ; 
    
The parse tree for the former is the tuple ("function",name,args,body), the parse tree for the latter is the tuple ("stmt",stmt). 

        optparams ->
        optparams -> params
        params -> IDENTIFIER , params
        params -> IDENTIFIER

optparams is a comma-separated list of zero or more identifiers. The parse tree for optparams is the list of all of the identifiers. 

        compoundstmt -> { statements } 
        statements -> stmt ; statements
        statements -> 

A compound statement is a list of zero or more statements, each of which is followed by a semicolon. (In real JavaScript, some statements do not need to be followed by a semicolon. For simplicity, we will assume that they all have to.) The parse tree for a compound statement is just the list of all of the statements. We will consider six kinds of possible statements: 

        stmt -> IF exp compoundstmt     
        stmt -> IF exp compoundstmt ELSE compoundstmt
        stmt -> IDENTIFIER = exp 
        stmt -> RETURN exp 

The "if", "assignment" and "return" statements should be familiar. It is also possible to use "var" statements in JavaScript to introduce new local variables (this is not necessary in Python): 

        stmt -> VAR IDENTIFIER = exp 

And it is also possible to treat an expression as a statement. This is 

        stmt -> exp 

The parse trees for statements are all tuples:
        
        ("if-then", conditional, then_branch)
        ("if-then-else", conditional, then_branch, else_branch)
        ("assign", identifier, new_value) 
        ("return", expression)
        ("var", identifier, initial_value) 
        ("exp", expression) 

To simplify things, for now we will assume that there is only one type of expression: identifiers that reference variables. In the next assignment, we'll encoding the parsing rules for expressions.

Recall the names of our tokens: 

'ANDAND',       # &&          | 'LT',           # <
'COMMA',        # ,           | 'MINUS',        # -
'DIVIDE',       # /           | 'NOT',          # !
'ELSE',         # else        | 'NUMBER',       # 1234 
'EQUAL',        # =           | 'OROR',         # ||
'EQUALEQUAL',   # ==          | 'PLUS',         # +
'FALSE',        # FALSE       | 'RBRACE',       # }
'FUNCTION',     # function    | 'RETURN',       # return
'GE',           # >=          | 'RPAREN',       # )
'GT',           # >           | 'SEMICOLON',    # ;
'IDENTIFIER',   # factorial   | 'STRING',       # "hello"
'IF',           # if          | 'TIMES',        # *
'LBRACE',       # {           | 'TRUE',         # TRUE
'LE',           # <=          | 'VAR',          # var 
'LPAREN',       # (           |

(3) Parsing Javascript Expressions:  In this exercise you will write a Parser for a subset of JavaScript. This will invole writing parsing rewrite rules (i.e., encoding a context-free grammar) and building up a parse tree (also called a syntax tree) of the result. This question may seem long at first, but it can be answered in a little over 50 lines. We have split the parsing of JavaScript into two exercises so that you have a chance to demonstrate your mastery of the concepts independently (i.e., so that you can get one of them right even if the other proves difficult). We could easily make a full JavaScript parser by putting all of the rules together. In this second parse, we wil handle JavaScript expressions. The JavaScript tokens we use will be the same ones we defined together in the Homework for Unit 2. (Even if you did not complete Homework 2, the correct tokens will be provided here.) Let's walk through our JavaScript expression grammar. We'll describe it somewhat informally in text: your job for this homework problem is to translate this description into a valid parser! First, there are a number of "base cases" in our grammar -- simple expressions that are not recursive. In each case, the abstract syntax tree is a simple tuple.

        exp -> IDENTIFIER       # ("identifier",this_identifier_value)
        exp -> NUMBER           # ("number",this_number_value)
        exp -> STRING           # ("string",this_string_value) 
        exp -> TRUE             # ("true","true") 
        exp -> FALSE            # ("false","false") 

There are also two unary expressions types -- expressions built recursively from a single child.

        exp -> NOT exp          # ("not", child_parse_tree)
        exp -> ( exp )          # child_parse_tree

For NOT, the parse tree is a simple tuple. For parentheses, the parse tree is even simpler: just return the child parse tree unchanged! 

There are many binary expressions. To deal with ambiguity, we have to assign them precedence and associativity.  I will list the lowest predecence binary operators first, and then continue in order of increasing precedence: 

        exp ->   exp || exp        # lowest precedence, left associative
        | exp && exp        # higher precedence, left associative 
        | exp == exp        # higher precedence, left associative
        | exp < exp         # /---
        | exp > exp         # | higher precedence, 
        | exp <= exp        # | left associative
        | exp >= exp        # \---
        | exp + exp         # /--- higher precedence,
        | exp - exp         # \--- left associative
        | exp * exp         # /--- higher precedence,
        | exp / exp         # \--- left associative

In each case, the parse tree is the tuple:
 
       ("binop", left_child, operator_token, right_child) 

For this assignment, the unary NOT operator has the highest precedence of all and is right associative. Finally, it is possible to have a function call as an expression:

       exp -> IDENTIFIER ( optargs ) 

The parse tree is the tuple ("call", function_name, arguments). 

       optargs -> 
       optargs -> args
       args -> exp , args
       args -> exp 

It is also possible to have anonymous functions (sometimes called lambda expressions) in JavaScript. 

       exp -> function ( optparams ) compoundstmt

However, for this assignment you are not responsible for lambda expressions. Arguments are comma-separated expressions. The parse tree for args or optargs is just the list of the parse trees of the component expressions. Recall the names of our tokens: 

     'ANDAND',       # &&          | 'LT',           # <
     'COMMA',        # ,           | 'MINUS',        # -
     'DIVIDE',       # /           | 'NOT',          # !
     'ELSE',         # else        | 'NUMBER',       # 1234 
     'EQUAL',        # =           | 'OROR',         # ||
     'EQUALEQUAL',   # ==          | 'PLUS',         # +
     'FALSE',        # FALSE       | 'RBRACE',       # }
     'FUNCTION',     # function    | 'RETURN',       # return
     'GE',           # >=          | 'RPAREN',       # )
     'GT',           # >           | 'SEMICOLON',    # ;
     'IDENTIFIER',   # factorial   | 'STRING',       # "hello"
     'IF',           # if          | 'TIMES',        # *
     'LBRACE',       # {           | 'TRUE',         # TRUE
     'LE',           # <=          | 'VAR',          # var 
     'LPAREN',       # (           |
