grammar Aa    ;
start         : ss EOF
              ;
ss            : s*
              ;
b             : '{' s* '}'
              ;
ifElse        : 'if' e b 'else' s
              ;
if_           : 'if' e b
              ;
while_        : 'while' e b
              ;
s             : b                            #blockStmt
              | ifElse                       #ifElseStmt
              | if_                          #ifStmt
              | while_                       #whileStmt
              | e ';'                        #expr
              | ';'                          #noOp
              ;
e             : STR+                         #str
              | FLOAT                        #float
              | NAME                         #name
              | '(' e ')'                    #paren
              | b                            #blockExpr
              | ifElse                       #ifElseExpr
              | if_                          #ifExpr
              | while_                       #whileExpr
              | '[' (e(','e)*)? ']'          #list
              | '{' (e':'e(','e':'e)*)? '}'  #dict
              | e '.' NAME                   #attr
              | e '(' (e (',' e)*)? ')'      #call
              | e '[' e ']'                  #getItem
              | NAME ':=' e                  #decl
              | NAME '=' e                   #assign
              | e '.' NAME '=' e             #attrAssign
              | e '[' e ']' '=' e            #setItem
              | '\\' NAME* ('*' var=NAME)? b #lambda
              ;
FLOAT         : [0-9]+ '.' [0-9]*
              |        '.' [0-9]+
              ;
INT           : [0-9]+
              ;
STR           :     ["] (~["] | '\\' ["]) * ["]
              |     ['] (~['] | '\\' [']) * [']
              | 'r' ["] (~["] | '\\' ["]) * ["]
              | 'r' ['] (~['] | '\\' [']) * [']
              ;
NAME          : [a-zA-Z0-9_$]+
              ;
CMT           : '#' ~'\n'* -> skip
              ;
WS            : [ \t\r\n]+ -> skip
              ;
