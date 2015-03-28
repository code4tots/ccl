grammar Ccl;
start      : stmts EOF
           ;
stmts      : (stmt? DELIM)*
           ;
stmt       : expr+                           #call
           | '{' stmts '}'                   #block
           | 'if' expr stmt 'else' stmt      #ifElse
           | 'if' expr stmt                  #if
           | 'while' expr stmt               #while
           | STR ':=' expr                   #decl
           | STR '=' expr                    #assign
           ;
expr       : STR                             #str
           | VAR                             #var
           | '\\' STR* '{' stmts '}'         #lambda
           | '[' expr* ']'                   #list
           | '[' (expr ':' expr)* ']'        #dict
           | '(' stmt ')'                    #cmd
           ;
DELIM      : ';' | '\n'
           ;
STR        : [a-zA-Z_0-9/\-+~.*]+
           | ["] (~["] | '\\' ["]) * ["]
           | ['] (~[']  | '\\' [']) * [']
           ;
VAR        : '$' [a-zA-Z_0-9$/\-+~.*]+
           ;
CMT        : '#' ~'\n'* -> skip
           ;
WS         : [ \t\r]+ -> skip
           ;
