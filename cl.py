"""cl
even simpler language
"""
from __future__ import print_function
from ply import lex, yacc

tokens = ('VALUE', 'NAME')
literals = '[],'
t_ignore = ' \t\n'
t_VALUE = (
    r'\d+\.?\d*|'
    r'\"(?:\\\"|[^"])*\"|'
    r"\'(?:\\\'|[^'])*\'")
t_NAME = r'(?!\d)[a-zA-Z0-9\\\-]+'
def t_error(t): raise Exception()

def p_zero_commands(p):
    "commands : "
    p[0] = []

def p_single_command(p):
    "commands : command"
    p[0] = [p[1]]

def p_commands(p):
    "commands : commands ',' command"
    p[0] = p[1]
    p[0].append(p[3])

def p_zero_atoms(p):
    "atoms : "
    p[0] = []

def p_atoms(p):
    "atoms : atoms atom"
    p[0] = p[1]
    p[0].append(p[2])

def p_command(p):
    "command : atom atoms"
    p[0] = CommandDisplay(p[1],p[2])

def p_name(p):
    "atom : NAME"
    p[0] = NameDisplay(p[1])

def p_literal(p):
    "atom : VALUE"
    p[0] = ValueDisplay(p[1])

def p_list(p):
    "atom : '[' commands ']'"
    p[0] = ListDisplay(p[2])

def p_all(p):
    "all : commands"
    p[0] = ListDisplay(p[1])

def p_error(p): raise Exception()

start = 'all'
lexer = lex.lex()
parser = yacc.yacc()

class Display(object):
    pass

class NameDisplay(Display):
    def __init__(self, name):
        self.name = name
    
    def find(self, scope):
        while self.name not in scope:
            scope = scope['__parent__']
        return scope
    
    def __call__(self, scope):
        return self.find(scope)[self.name]

class ValueDisplay(Display):
    def __init__(self, value):
        self.value = eval(value)
    
    def __call__(self, scope):
        return self.value

class ListDisplay(Display):
    def __init__(self, commands):
        self.commands = commands
    
    def __call__(self, scope):
        return [command(scope) for command in self.commands]

class CommandDisplay(Display):
    def __init__(self, f, args):
        self.f = f
        self.args = args
    
    def __call__(self, scope):
        f = self.f(scope)
        
        if isinstance(f, SpecialForm):
            return f(scope, self.args)
        
        if callable(f):
            return f(*[arg(scope) for arg in self.args])
        
        return f

class SpecialForm(object):
    def __init__(self, f):
        self.f = f
    
    def __call__(self, scope, args):
        return self.f(scope, args)

def run(string, scope):
    return parser.parse(string, lexer=lexer)(scope)

global_scope = {
    'print' : print
}

run("""
print [1, 2, 3]



""",
global_scope)
