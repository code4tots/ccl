"""Hmm. Maybe a bit more conventional language.

But with complete dependency injection.
"""

from ply import lex, yacc

tokens = ('NAME', 'FLOAT', 'INT', 'STRING')
literals = '().'
t_ignore = ' \t\n'
t_NAME = r'(?!\d)\w+'
t_FLOAT = r'\d+\.\d+'
t_INT = r'\d+(?!\.)'
t_STRING = r'\"(?:\\\"|[^"])*\"'
lexer = lex.lex()

def p_dot_expression(p):
  """expression : expression '.' NAME"""


program = """
(w.add 1 2)

"""
