class SpecialForm(object):
    """Marker for functions that are passed scope and argument list
    rather than evaluated arguments.
    """
    def __init__(self, f):
        self.f = f
    
    def __call__(self, scope, args):
        return self.f(scope, args)

class Location(object):
    def __init__(self, filename, string, lexpos, lineno):
        self.string = string
        self.lexpos = lexpos
        self.lineno = lineno

class Display(object):
    """Display is essentially an abstract syntax tree
    """

class LiteralDisplay(Display):
    def __init__(self, value):
        self.value = value
    
    def __call__(self, scope):
        return self.value

class NameDisplay(Display):
    def __init__(self, name):
        self.name = name
    
    def find(self, scope):
        name = self.name
        original_scope = scope
        while name not in scope and '__parent__' in scope:
            scope = scope['__parent__']
        if name not in scope:
            raise KeyError(name)
        return scope
    
    def __call__(self, scope):
        return self.find(scope)[self.name]

class CommandDisplay(Display):
    def __init__(self, f, args):
        self.f = f
        self.args = args
    
    def __call__(self, scope):
        f = self.f(scope)
        if isinstance(f, SpecialForm):
            return f(scope, self.args)
        else:
            return f(*[arg(scope) for arg in self.args])

class ListDisplay(Display):
    def __init__(self, atoms):
        self.atoms = atoms
    
    def __call__(self, scope):
        return [atom(scope) for atom in self.atoms]

class BlockDisplay(Display):
    def __init__(self, commands):
        self.commands = commands
    
    def __call__(self, scope):
        last = None
        for command in self.commands:
            last = command(scope)
        return last

from ply import lex
from ply import yacc

tokens = ('STRING', 'INT', 'FLOAT', 'NAME', 'NEWLINE')
literals = '{}[];.'
t_ignore = ' \t'

def token_action(convert):
    def function(t):
        t.value = convert(t.value)
        return t
    return function

def token_literal_action(convert):
    return token_action(lambda x : LiteralDisplay(convert(x)))

t_STRING = lex.TOKEN(
    r'\"(?:\\\"|[^"])*\"|'
    r"\'(?:\\\'|[^'])*\'")(token_literal_action(eval))
t_INT = lex.TOKEN(r'\d+(?!\.)')(token_literal_action(int))
t_FLOAT = lex.TOKEN(r'\d+\.\d*')(token_literal_action(float))
t_NAME = lex.Token(r'[a-zA-Z_][a-zA-Z_0-9\-]*')(token_action(NameDisplay))

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    return t

lexer = lex.lex()

def p_token_atom(p):
    """atom : STRING
            | INT
            | FLOAT
            | NAME"""
    p[0] = p[1]

def p_block(p):
    "atom : '{' command_list '}'"
    p[0] = BlockDisplay(p[2])

def p_singleton_block(p):
    "atom : '{' command '}'"
    p[0] = BlockDisplay([p[2]])

def p_list(p):
    "atom : '[' atom_list ']'"
    p[0] = ListDisplay(p[2])

def p_attribute(p):
    "atom : atom '.' NAME"
    p[0] = CommandDisplay(
        NameDisplay('getattr'),
        (p[1],LiteralDisplay(p[3].name)))

def p_command(p):
    'command : atom atom_list'
    p[0] = CommandDisplay(p[1],p[2])

def p_empty_command_list(p):
    'command_list : '
    p[0] = []

def p_command_list_with_newline(p):
    'command_list : command_list NEWLINE'
    p[0] = p[1]

def p_command_list(p):
    'command_list : command_list NEWLINE command'
    p[0] = p[1]
    p[0].append(p[3])

def p_empty_atom_list(p):
    'atom_list : '
    p[0] = []

def p_atom_list(p):
    'atom_list : atom_list atom'
    p[0] = p[1]
    p[0].append(p[2])

def p_all(p):
    'all : command_list'
    p[0] = BlockDisplay(p[1])

start = 'all'

parser = yacc.yacc()

def parse(string):
    return parser.parse(string, lexer=lexer)

def main():
    from ccl.pylib import builtin_scope
    parse('''

let x [1 2 3]
print x
let y 77
print [x y]
print {[1 2].__len__}

''')(builtin_scope)

if __name__ == '__main__':
    main()
