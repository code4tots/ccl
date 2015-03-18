grammar Ccl;

start : stmts
      ;

stmts : stmt*
      ;

stmt : expr ';'
     ;

exprs : expr (',' expr)*
      ;

expr : atom=INT #intExpr
     | atom=ID #idExpr
     | fn=expr '(' ')' #callExpr
     | fn=expr '(' args=exprs ')' #callExpr
     | left=expr op=('*'|'/') right=expr #binOpExpr
     | left=expr op=('+'|'-') right=expr #binOpExpr
     ;

INT : ('0'..'9')+
    ;

ID : [a-zA-Z_][a-zA-Z_0-9]*
   ;

WS : [ \t\r\n]+ -> skip
   ;
