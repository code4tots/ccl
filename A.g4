grammar A     ;
start         : s* ;
m             : ('\n' | ';') ;
r             : m? c m ;
s             : m | r ;
b             : '{' s* '}' ;
c             : 'if' r r 'else' r #ifElse
              | e+ #call ;
e             : STR+ #str
              | NAME #name
              | b #block
              | '(' c ')' #callExpr
              | '['(e(','e)*)?']' #list
              | '{'(e':'e(','e':' e)*)?'}' #dict
              | '\\' NAME* b #lambda ;
FLOAT         : [0-9]+ '.' [0-9]* 
              |        '.' [0-9]+ ;
INT           : [0-9]+ ;
STR           :     ["] (~["] | '\\' ["]) * ["]
              |     ['] (~['] | '\\' [']) * [']
              | 'r' ["] (~["] | '\\' ["]) * ["]
              | 'r' ['] (~['] | '\\' [']) * ['] ;
NAME          : [a-zA-Z0-9_$]+ ;
CMT           : '#' ~'\n'* -> skip ;
WS            : [ \t\r\n]+ -> skip ;
