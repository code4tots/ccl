grammar Kyumin;
start         : ss EOF
              ;
ss            : s*
              ;
b             : '{' s* '}'
              ;
s             : b                            #blockStmt
              | 'if' e b 'else' s            #ifElse
              | 'if' e b                     #if
              | 'while' e b                  #while
              | e ';'                        #expr
              | ';'                          #noOp
              ;
e             : STR                          #str
              | FLOAT                        #float
              | INT                          #int
              | NAME                         #name
              | b                            #blockExpr
              | '[' (e(','e)*)? ']'          #list
              | '{' (e':'e(','e':'e)*)? '}'  #dict
              | e '.' NAME                   #attr
              | e '(' (e (',' e)*)? ')'      #call
              | e '[' e ']'                  #getItem
              | e op=('*'|'/'|'//'|'%') e    #binop
              | e op=('+'|'-') e             #binop
              | e op=( '<'
                     | '<='
                     | '>'
                     | '>='
                     ) e                     #binop
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
