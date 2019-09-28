# Parsing

JavaScript allows function calls:
    
    myfun(11,12)
    'exp : IDENTIFIER LPAREN optargs RPAREN'

We want the parse tree to be:  ("call", "myfun", [("number", 11), ("number", 12)]).
