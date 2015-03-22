grammar Ccl;

start : stmts
      ;

stmts : stmt*
      ;

stmt : expr ';'
     ;

exprs : expr (',' expr)*
      |
      ;

exprPairs : expr ':' expr (',' expr ':' expr)*
          |
          ;

block : '{' stmts '}'
      ;

expr : atom=NUM #numExpr
     | atom=STR #strExpr
     | atom=ID #idExpr
     | '(' expr ')' #parExpr
     | '[' exprs ']' #listExpr
     | fn=expr '(' args=exprs ')' #callExpr
     | left=expr op=('*'|'/') right=expr #binOpExpr
     | left=expr op=('+'|'-') right=expr #binOpExpr
     ;

NUM : ('0'..'9')+ '.'? ('0'..'9')*
    | '.' ('0'..'9')+
    ;

STR : ["] (~["] | '\\' ["]) * ["]
    | ['] (~['] | '\\' [']) * [']
    ;

ID : [a-zA-Z_0-9]+
   ;

WS : [ \t\r\n]+ -> skip
   ;
