grammar Bub;

start  : stmts
       ;

stmts  : stmt*
       ;

stmt   : cmd ('\n' | ' ;' | EOF)
       | '\n'
       | ';'
       ;

cmd    : expr args                        #call
       | 'while' expr cmd                 #while
       | '{' stmts '}'                    #block
       | name=ID ':=' expr                #declaration
       | name=ID '='  expr                #assignment
       ;

expr   : atom=NUM                         #num
       | atom=STR                         #str
       | atom=ID                          #id
       | '\\' id* block                   #lambda
       | '(' cmd ')'                      #cmdExpr
       ;

args   : (arg | kwarg)*
       ;

arg    : expr
       ;

kwarg  : name=ID '=' expr
       ;

argids : argid*
       ;

argid  : name=ID
       ;

NUM    : ('0'..'9')+ '.'? ('0'..'9')*
       | '.' ('0'..'9')+
       ;

STR    : ["] (~["] | '\\' ["]) * ["]
       | ['] (~[']  | '\\' [']) * [']
       ;

ID     : [a-zA-Z_0-9$/\-+~.]+
       ;

CMT    : '#' ~'\n'* -> skip
       ;

WS     : [ \t\r]+ -> skip
       ;
