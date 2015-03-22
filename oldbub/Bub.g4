grammar Bub;

start : stmts
      ;

stmts : stmt*
      ;

stmt  : cmd ('\n' | ';' | EOF)
      | '\n'
      | ';'
      ;

ids   : ID*
      ;

expr  : atom=NUM                 #numExpr
      | atom=STR                 #strExpr
      | atom=ID                  #idExpr
      | '(' cmd ')'              #cmdExpr
      | '\\' ids '{' stmts '}'   #lambdaExpr
      ;

arg   : expr
      ;

kwarg : ID '=' expr
      ;

args  : (arg | kwarg) *
      ;

cmd   : expr args                  #basicCmd
      | '{' stmts '}'              #blockCmd
      | 'while' expr '{' stmts '}' #whileCmd
      | cmd '>' expr               #redirectCmd
      | name=ID ':=' value=cmd     #declareCmd
      | name=ID '=' value=cmd      #assignCmd
      ;

NUM   : ('0'..'9')+ '.'? ('0'..'9')*
      | '.' ('0'..'9')+
      ;

STR   : ["] (~["] | '\\' ["]) * ["]
      | ['] (~['] | '\\' [']) * [']
      ;

ID    : [a-zA-Z_0-9$/\-~.]+
      ;

CMT   : '#' ~'\n'* -> skip
      ;

WS    : [ \t\r]+ -> skip
      ;
