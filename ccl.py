"""This time, completely ignore extensibility.

Just make it a language I would want to use for fun.

MAKE IT FUN.

"""

from ply import lex, yacc

keywords = {keyword : keyword.upper() for keyword in ['if', 'then', 'else']}
symbols = {'++' : 'INCREMENT', '--' : 'DECREMENT'}
literals = '()[]{}.,+-=/*'

t_ignore = ' \t\n'
t_NAME = r'(?!\d)\w+'
t_FLOAT = r'\-?\+?\d+\.\d*'
t_INT = r'\-?\+?\d+(?!\.)'
t_STRING = r'\"(?:\\\"|[^"])*\"'
t_STRING += t_STRING.replace('"',"'")

tokens = ['NAME','FLOAT','INT','STRING'] + list(symbols.values()) + list(keywords.values())

def p_all(p):
    "all : expression_list"
    def all_(scope):
        last = None
        for expression in p[1]:
            last = expression(scope)
        return last
    p[0] = all_

def p_empty_expression_list(p):
    "expression_list : "
    p[0] = []

def p_expression_list_with_commas(p):
    "expression_list : expression_list ',' "
    p[0] = p[1]

def p_expression_list(p):
    "expression_list : expression_list expression"
    p[0] = p[1]; p[0].append(p[2])

def p_name(p):
    "expression : NAME"
    p[0] = lambda scope : scope[p[1]]

def p_literal(p):
    """expression : FLOAT
                  | INT
                  | STRING"""
    p[0] = lambda scope : eval(p[1])

def p_function_call(p):
    "expression : expression '[' expression_list ']'"
    def function_call(scope):
        return p[1](scope)(*[e(scope) for e in p[3]])
    p[0] = function_call

lexer = lex.lex()
parser = yacc.yacc()

parser.parse("""
print [1 2 3]

""", lexer=lexer)({'print' : print})
