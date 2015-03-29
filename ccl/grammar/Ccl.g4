grammar Ccl;
start      : ss EOF
           ;
ss         : s*
           ;
s          : e ';'                        #expression
           ;
e          : STR                          #str
           | FLOAT                        #float
           | INT                          #int
           | NAME                         #name
           | e '(' (e (',' e)*)? ')'      #call
           ;
FLOAT      : [0-9]+ '.' [0-9]*
           |        '.' [0-9]+
           ;
INT        : [0-9]+
           ;
STR        :     ["] (~["] | '\\' ["]) * ["]
           |     ['] (~['] | '\\' [']) * [']
           | 'r' ["] (~["] | '\\' ["]) * ["]
           | 'r' ['] (~['] | '\\' [']) * [']
           ;
NAME       : [a-zA-Z0-9_$]+
           ;
CMT        : '#' ~'\n'* -> skip
           ;
WS         : [ \t\r\n]+ -> skip
           ;
