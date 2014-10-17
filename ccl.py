"""ccl
"""
### import
import re
import os
import operator

### misc
class Location(object):
    def __init__(self, string, path, position):
        self.string = string
        self.path = path
        self.position = position
    
    @property
    def line_begin(self):
        return self.string.rfind('\n', 0, self.position) + 1
    
    @property
    def line_end(self):
        e = self.string.find('\n', self.position, len(self.string))
        return len(self.string) if e == -1 else e
    
    @property
    def line(self):
        return self.string[self.line_begin:self.line_end]
    
    @property
    def line_number(self):
        return 1 + self.string.count('\n', 0, self.position)
    
    @property
    def column_number(self):
        return 1 + self.position - self.line_begin
    
    @property
    def column_star(self):
        return (self.column_number - 1) * ' ' + '*'
    
    def __str__(self):
        return 'In %r on line %s, column %s\n%s\n%s' % (
            self.path,
            self.line_number,
            self.column_number,
            self.line,
            self.column_star)

class Token(object):
    def __init__(self, location, type_, value):
        self.location = location
        self.type = type_
        self.value = value

class SpecialForm(object):
    def __init__(self, f, name):
        self.f = f
        self.name = name
    
    def __call__(self, scope, args):
        return self.f(scope, args)

### display
class Display(object):
    def execute_with_callstack(self, scope, f):
        get_global(scope, '__call_stack__').append(self.location)
        try:
            value = f()
        except Exception as e:
            if not hasattr(e, 'stack_trace'):
                e.stack_trace = tuple(get_global(scope, '__call_stack__'))
                
            raise
        finally:
            get_global(scope, '__call_stack__').pop()
        return value

class LiteralDisplay(Display):
    def __init__(self, location, value_string):
        self.location = location
        self.value = eval(value_string)
    
    def __call__(self, scope):
        return self.value

class NameDisplay(Display):
    def __init__(self, location, name):
        self.location = location
        self.name = name
    
    def __call__(self, scope):
        def f():
            return find_scope(scope, self.name)[self.name]
        return self.execute_with_callstack(scope, f)

class CommandDisplay(Display):
    def __init__(self, location, f, args):
        self.location = location
        self.f = f
        self.args = args
    
    def __call__(self, scope):
        f = self.f(scope)
        args = (
            self.args if isinstance(f, SpecialForm) else
            [arg(scope) for arg in self.args])
        
        def ff():
            return (
                f(scope, args) if isinstance(f, SpecialForm) else 
                f(*args))
        
        return self.execute_with_callstack(scope, ff)

class ListDisplay(Display):
    def __init__(self, location, atoms):
        self.location = location
        self.atoms = atoms
    
    def __call__(self, scope):
        return [atom(scope) for atom in self.atoms]

class BlockDisplay(Display):
    def __init__(self, location, commands):
        self.location = location
        self.commands = commands
    
    def __call__(self, scope):
        last = None
        for command in self.commands:
            last = command(scope)
        return last

### lexer
space_re = re.compile(r'[ \t]*')
symbols = '{}[]$.'
type_regex_pairs = tuple(
    (symbol, re.compile(re.escape(symbol))) for symbol in symbols
    ) + tuple((t,re.compile(r)) for t, r in (
        ('\n', r'\n\s*'),
        ('string',
            r'\"(?:\\\"|[^"])*\"|'
            r"\'(?:\\\'|[^'])*\'"),
        ('float', r'\d+\.\d*'),
        ('int', r'\d+'),
        ('name', r'[0-9a-zA-Z_\-]+')))

def lex(string, path):
    s = space_re
    i = s.match(string).end()
    p = type_regex_pairs
    
    def here():
        return Location(string, path, i)
    
    while i < len(string):
        location = here()
        
        for type_, regex in p:
            match = regex.match(string, i)
            if match is not None:
                value = match.group()
                yield Token(location, type_, value)
                i = match.end()
                break
        else:
            # TODO: smarter exception handling
            raise Exception()
        
        i = s.match(string, i).end()
    
    yield Token(here(), 'end', None)

### parser
def parse(string, path):
    token_generator = lex(string, path)
    lookahead = [next(token_generator)]
    
    def here():
        return lookahead[0].location
    
    def at(type_):
        return lookahead[0].type == type_
    
    def step():
        last = lookahead[0]
        lookahead[0] = next(token_generator)
        return last
    
    def consume(type_):
        if at(type_):
            return step()
    
    def expect(type_):
        if not at(type_):
            # TODO: smarter exception handling
            raise Exception()
        return step()
    
    def newlines():
        while at('\n'):
            step()
    
    def at_atom_start():
        return lookahead[0].type in ('{','(','int','float','string','name')
    
    def atom_sequence(production, skip):
        def sequence_production():
            skip()
            items = []
            while at_atom_start():
                items.append(production())
                skip()
            return items
        return sequence_production
    
    def command():
        f = atom()
        args = arguments()
        
        if consume('$'):
            args.append(command())
        
        return CommandDisplay(f.location, f, args)
    
    def atom():
        location = here()
        if consume('{'):
            block = BlockDisplay(location, commands())
            expect('}')
            return_value = block
        elif consume('['):
            list_ = ListDisplay(location, list_items())
            expect(']')
            return_value = list_
        elif at('name'):
            return_value = NameDisplay(location, step().value)
        else:
            return_value = LiteralDisplay(location, step().value)
        
        dot_location = here()
        while consume('.'):
            if not at('name'):
                # TOOD: smart exception
                raise Exception()
            
            name_location = here()
            
            return_value = CommandDisplay(
                dot_location,
                NameDisplay(dot_location, 'getattr'),
                [
                    return_value,
                    LiteralDisplay(
                        name_location,
                        "'" + step().value + "'")])
            
            dot_location = here()
        
        return return_value
    
    def all_():
        location = here()
        block = BlockDisplay(location, commands())
        if not at('end'):
            # TODO: smarter exception handling
            raise Exception()
        return block
    
    commands = atom_sequence(command, skip=newlines)
    arguments = atom_sequence(atom, skip=lambda : None)
    list_items = atom_sequence(atom, skip=newlines)
    
    return all_()

### builtins
builtins_scope = dict()
builtins_scope.update({
    
    'lt' : operator.lt,
    'gt' : operator.gt,
    
    'print' : print,
    'getattr' : getattr})

def special_form(name):
    def wrapper(f):
        builtins_scope[name] = form = SpecialForm(f, name)
        return f
    return wrapper

def function(name):
    def wrapper(f):
        builtins_scope[name] = f
        return f
    return wrapper

### api
@special_form('import')
def import_(scope, args):
    path_display, = args
    path = path_display(scope)
    return load(scope, path)

@function('load')
def load(scope, path):
    path = os.path.realpath(path)
    with open(path) as f:
        contents = f.read()
    module_scope = new_module_scope(scope)
    parse(contents, path)(module_scope)
    return scope

### scope
@function('get-global')
def get_global(scope, key):
    return scope['__global__'][key]

@function('find-scope')
def find_scope(scope, key):
    while key not in scope and '__parent__' in scope:
        scope = scope['__parent__']
    return scope

@function('new-scope')
def new_scope(parent):
    scope = dict()
    scope.update({
        '__parent__' : parent,
        '__global__' : parent['__global__'],
        '__builtins__' : parent['__builtins__'],
        '__scope__' : scope})
    return scope

@function('new-module-scope')
def new_module_scope(parent):
    scope = new_scope(parent)
    return scope

@function('new-global-scope')
def new_global_scope():
    scope = dict()
    scope.update({
        'True' : True,
        'False' : False,
        '__call_stack__'  : [],
        '__imports__' : dict(),
        '__parent__' : builtins_scope,
        '__global__' : scope,
        '__builtins__' : builtins_scope,
        '__scope__' : scope})
    return scope

### main
def main():
    from sys import argv
    try:
        load(new_global_scope(), argv[1])
    except Exception as e:
        print(type(e).__name__)
        print(str(e))
        for location in e.stack_trace:
            print(location)

def debug():
    from sys import argv
    load(new_global_scope(), argv[1])

if __name__ == '__main__':
    main()
