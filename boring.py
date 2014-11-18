"""Hmm. Maybe a bit more conventional language.
"""

from ply import lex, yacc

tokens = ('NAME', 'FLOAT', 'INT', 'STRING')
literals = '[]'
t_ignore = ' \t\n'
t_NAME = r'(?!\d)\w+'
t_FLOAT = r'\d+\.\d+'
t_INT = r'\d+(?!\.)'
t_STRING = r'\"(?:\\\"|[^"])*\"'

program = """

[
    x = 3
    
]
"""