grammar A     ;
start         : s* ;
m             : ('\n' | ';') ;
r             : m? c (m | EOF) ;
s             : m | r ;
b             : '{' s* '}' ;
c             : e+ ;
e             : STR+ #str
              | NAME #name
              | b #block
              | '(' c ')' #callExpr
              | 'if' e r 'else' r #ifElse
              | 'if' e r #if_
              ;
FLOAT         : [0-9]+ '.' [0-9]* 
              |        '.' [0-9]+ ;
INT           : [0-9]+ ;
STR           :     ["] (~["] | '\\' ["]) * ["]
              |     ['] (~['] | '\\' [']) * [']
              | 'r' ["] (~["] | '\\' ["]) * ["]
              | 'r' ['] (~['] | '\\' [']) * ['] ;
NAME          : [a-zA-Z0-9_$]+ ;
CMT           : '#' ~'\n'* -> skip ;
WS            : [ \t\r]+ -> skip ;
