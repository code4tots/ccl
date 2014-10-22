"""Language that transforms to C++

C++ has a monster of a grammar.

So I am going to write a language that translates
to C++, so that I can write my other language in
a more manageable format.

"""
from location import Location

from ply import lex, yacc

symbols = {
    '==' : 'EQUAL',
    '!=' : 'NOT_EQUAL'}

keywords = {
    'template' : 'TEMPLATE'}

literals = ';(){}[]'
t_ignore = ' \t\n'
t_STRING = r'\"(?:\\\"|[^"])\"'
t_FLOAT = r'[0-9]+\.[0-9]*'
t_INT = r'[0-9]+(?!\.)'
t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'

tokens = ('STRING', 'FLOAT', 'INT', 'NAME'
    ) + tuple(symbols.values()
    ) + tuple(keywords.values())

def t_error(t):
    # TODO better error handling
    raise Exception()

lexer = lex.lex()

