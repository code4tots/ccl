grammar Ccl   ;
start         : s*
              ;
b             : '{' s* '}'
              ;
ifElse        : 'if' e b 'else' s
              ;
while_        : 'while' e b
              ;
h             : b
              | ifElse
              | while_
              ;
s             : h
              | e ';'
              | ';'
              ;
e             : STR+ #str
              | NAME #name
              | '['(e(','e)*)?']' #list
              | '{'(e':'e(','e':' e)*)?'}' #dict
              | '(' e ')' #par
              | e '('(e(',' e)*)?')' #call
              | e '[' e ']' #getItem
              | e '[' e ']' '=' e #setItem
              | NAME op=(':='|'=') e #assign
              | '\\' NAME* b #lambda
              | h #hybrid
              ;
STR           : [0-9]+ '.' [0-9]*
              |        '.' [0-9]+
              | [0-9]+
              |     ["] (~["] | '\\' ["]) * ["]
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