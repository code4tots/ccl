class SpecialForm(object):
    """Marker for functions that are passed scope and argument list
    rather than evaluated arguments.
    """
    def __init__(self, f, name=None):
        self.f = f
        self.name = str(id(self)) if name is None else name
    
    def __call__(self, scope, args):
        return self.f(scope, args)
    
    def __str__(self):
        return '<SpecialForm %s>' % (self.name,)

class Display(object):
    """Display is essentially an abstract syntax tree
    
    location based attributes:
        file_name
        string
        lexpos
    """
    @property
    def location_string(self):
        return "In %r line %s column %s:\n%s\n%s" % (
            self.file_name,
            self.line_number,
            self.column_number,
            self.line,
            self.column_star)
    
    @property
    def line(self):
        return self.string[self.line_begin:self.line_end]
    
    @property
    def line_begin(self):
        return self.string.rfind('\n', 0, self.lexpos) + 1
    
    @property
    def line_end(self):
        end = self.string.find('\n', self.lexpos)
        if end == -1:
            end = len(self.string)
        return end
    
    @property
    def line_number(self):
        return self.string[:self.lexpos].count('\n') + 1
    
    @property
    def column_number(self):
        return self.lexpos - self.line_begin + 1
    
    @property
    def column_star(self):
        return (self.column_number - 1) * ' ' + '*'

class LeafDisplay(Display):
    def walk(self, f):
        f(self)

class LiteralDisplay(LeafDisplay):
    def __init__(self, value):
        self.value = value
    
    def __call__(self, scope):
        return self.value

class NameDisplay(LeafDisplay):
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
        scope['__global__']['__call_stack__'].append(self)
        try:
            result = self.find(scope)[self.name]
        except Exception:
            raise
        else:
            scope['__global__']['__call_stack__'].pop()
        return result

class BranchDisplay(Display):
    def walk(self, f):
        f(self)
        for display in self:
            display.walk(f)

class CommandDisplay(BranchDisplay):
    def __init__(self, f, args):
        self.f = f
        self.args = args
    
    def __call__(self, scope):
        f = self.f(scope)
        
        if not isinstance(f, SpecialForm):
            args = [arg(scope) for arg in self.args]
        
        scope['__global__']['__call_stack__'].append(self)
        try:
            if isinstance(f, SpecialForm):
                result = f(scope, self.args)
            else:
                result = f(*args)
        except Exception:
            raise
        else:
            scope['__global__']['__call_stack__'].pop()
            
        return result
    
    def __iter__(self):
        yield self.f
        for arg in self.args:
            yield arg

class ListDisplay(BranchDisplay):
    def __init__(self, atoms):
        self.atoms = atoms
    
    def __call__(self, scope):
        return [atom(scope) for atom in self.atoms]
    
    def __iter__(self):
        return iter(self.atoms)

class BlockDisplay(BranchDisplay):
    def __init__(self, commands):
        self.commands = commands
    
    def __call__(self, scope):
        last = None
        for command in self.commands:
            last = command(scope)
        return last
    
    def __iter__(self):
        return iter(self.commands)

from ply import lex
from ply import yacc

tokens = ('STRING', 'INT', 'FLOAT', 'NAME', 'NEWLINE')
literals = '{}[].$'
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
    p[0].lexpos = p.lexpos(1)

def p_block(p):
    "atom : '{' command_list '}'"
    p[0] = BlockDisplay(p[2])
    p[0].lexpos = p.lexpos(1)

def p_singleton_block(p):
    "atom : '{' command '}'"
    p[0] = BlockDisplay([p[2]])
    p[0].lexpos = p.lexpos(1)

def p_list(p):
    "atom : '[' atom_list ']'"
    p[0] = ListDisplay(p[2])
    p[0].lexpos = p.lexpos(1)

def p_attribute(p):
    "atom : atom '.' NAME"
    p[0] = CommandDisplay(
        NameDisplay('getattr'),
        (p[1],LiteralDisplay(p[3].name)))
    p[0].lexpos = p[1].lexpos

def p_command(p):
    'command : atom atom_list'
    p[0] = CommandDisplay(p[1],p[2])
    p[0].lexpos = p[1].lexpos

def p_command_sugar(p):
    "command : atom atom_list '$' command"
    p[2].append(p[4])
    p[0] = CommandDisplay(p[1],p[2])
    p[0].lexpos = p[1].lexpos

def p_singleton_command_list(p):
    'command_list : command'
    p[0] = [p[1]]

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
    p[0].lexpos = p.lexpos(1)

start = 'all'

parser = yacc.yacc()

def parse(string, file_name=''):
    display = parser.parse(string, lexer=lexer)
    
    @display.walk
    def f(d):
        d.string = string
        d.file_name = file_name
    
    return display

def run_string(string, file_name, scope):
    import ccl.pylib
    return parse(string, file_name)(scope)

def quick_run_string(string):
    from ccl.pylib import builtin_scope, new_scope, print_exception_message
    scope = new_scope(builtin_scope)
    try:
        return parse(string)(scope)
    except Exception as e:
        print_exception_message(e, scope['__global__']['__call_stack__'])

def load_module(realpath, parent_scope = None):
    import os
    from ccl.pylib import new_scope
    
    if parent_scope is None:
        from ccl.pylib import builtin_scope
        parent_scope = builtin_scope
    
    with open(realpath) as f:
        string = f.read()

    module_scope = new_scope(parent_scope)
    run_string(string, realpath, module_scope)

    return module_scope

def run_script(path):
    from ccl.pylib import builtin_scope, print_exception_message
    try:
        load_module(path)
    except Exception as e:
        print_exception_message(e, builtin_scope['__call_stack__'])
