grammar Bub;
start      : stmts
           ;
stmts      : stmt*
           ;
stmt       : cmd DELIM
           | DELIM
           ;
cmd        : expr+                           #call
           | '{' stmts '}'                   #block
           | 'if' expr stmt 'else' stmt      #ifElse
           | 'if' expr stmt                  #if
           | 'while' expr stmt               #while
           | ID ':=' expr                    #declaration
           | ID '='  expr                    #assignment
           ;
expr       : NUM                             #num
           | STR                             #str
           | ID                              #id
           | '\\' ID* '{' stmts '}'          #lambda
           | '[' expr* ']'                   #list
           | '[' (expr ':' expr)* ']'        #dict
           | '(' cmd ')'                     #cmdExpr
           ;
DELIM      : ';' | '\n' | EOF
           ;
NUM        : ('0'..'9')+ '.'? ('0'..'9')*
           | '.' ('0'..'9')+
           ;
STR        : ["] (~["] | '\\' ["]) * ["]
           | ['] (~[']  | '\\' [']) * [']
           ;
ID         : [a-zA-Z_0-9$/\-+~.]+
           ;
CMT        : '#' ~'\n'* -> skip
           ;
WS         : [ \t\r]+ -> skip
           ;
