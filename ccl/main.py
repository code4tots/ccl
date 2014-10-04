"""
ccl.main

The 'engine' of the interpreter.

I was kind of lazy and put a lot of functionality in this one file.
I hope you can forgive me.

To make navigation a bit more manageable, this file is split into
several sections, marked by comments starting with three '#'.

For your convenience, the sections are named

    imports
    lexer
    parser
    ast (abstract syntax tree)
    context
    repl

Each one of these sections (except imports), could probably have
comprised of a file in itself.

However, at ~300 lines, this file is still rather manageable.

"""
### imports
import re

### lexer
literals = '()[]{}.;\n'
tokens = tuple((t, re.compile(r)) for t, r in (
    ('String', r'\"(?:\\\"|[^"])*\"' '|' r"\'(?:\\\'|[^'])*\'"),
    ('Float' , r'\-?\d+\.\d*|\-?\.\d+'),
    ('Int'   , r'\-?\d+'),
    ('Name'  , r'\w+')) +
    tuple((s, re.escape(s)) for s in literals))

class Token(object):
    def __init__(self, type_, value, lex_position, line_number, file_name,
            string):
        self.type = type_
        self.value = value
        self.lex_position = lex_position
        self.line_number = line_number
        self.file_name = file_name
        self.string = string
    
    def location_string(self):
        begin = self.string.rfind('\n', 0, self.lex_position) + 1
        end = self.string.find('\n', self.lex_position + 1)
        if end == -1:
            end = len(self.string)
        return 'In file %r on line %s:\n%s' % (
            self.file_name, self.line_number, self.string[begin : end])

def lex(string, file_name = ''):
    s = string   # string to parse (aliased for convenience)
    i = 0        # current lex position
    p = tokens   # token type regex pairs
    l = 1        # line number
    while i < len(s) and s[i] in ' \t': i += 1
    while i < len(s):
        for t, r in tokens:
            m = r.match(s, i)
            if m is not None:
                g = m.group()
                yield Token(t, g, i, l, file_name, s)
                i = m.end()
                l += g.count('\n')
                break
        else:
            m = re.compile(r'\S*').match(s, i)
            Token(t, m.group(), i, l, file_name, s).error('unrecognized token')
        while i < len(s) and s[i] in ' \t': i += 1
    yield Token(None, None, i, l, file_name, s)

### parser
def parse(string, file_name = ''):
    generator = lex(string, file_name)
    lookahead = [next(generator)]
    
    def next_token():
        token = lookahead[0]
        lookahead[0] = next(generator)
        return token
    
    def expect(t):
        if lookahead[0].type == t:
            raise SyntaxError()
        return next_token()
    
    def consume(t):
        return lookahead[0].type == t
    
    def multiple(rule, skip_newlines):
        elements = []
        
        while True:
            if skip_newlines:
                skip_lines()
            
            if lookahead[0].type not in rule.start_symbols:
                break
            
            elements.append(rule())
        
        return elements
    
    def skip_lines():
        while lookahead[0].type in (';','\n'):
            next_token()
    
    def all_():
        return Block(
            Token(None, None, 0, 1, file_name, string),
            multiple(command, skip_newlines=True))
    
    def atom():
        if lookahead[0].type.isalpha():
            t = lookahead[0].type
            r = globals()[t+'Display'](next_token())
        elif lookahead[0].type == '[':
            r = ListDisplay(
                next_token(),
                multiple(atom, skip_newlines=True))
            expect(']')
        elif consume('('):
            r = command()
            expect(')')
        elif lookahead[0].type == '{':
            r = Block(
                next_token(),
                multiple(command, skip_newlines=True))
            expect('}')
        else:
            raise SyntaxError('expected atom')
        
        while consume('.'):
            r = AttributeDisplay(r, expect('NAME').value)
        
        return r
    
    def command():
        f = atom()
        args = multiple(atom, skip_newlines=False)
        return Command(f,args)
    
    atom.start_symbols = (
        'String', 'Float', 'Int', 'Name',
        '(', '{', '[')
    
    command.start_symbols = atom.start_symbols
    
    return all_()

### ast (abstract syntax tree)
class AbstractSyntaxTree(object):
    def __call__(self, ctx):
        try: return self.call(ctx)
        except BaseException as e:
            if not hasattr(e, 'ast_stack'):
                e.ast_stack = []
            e.ast_stack.append(self)
            raise

class TokenDisplay(AbstractSyntaxTree):
    def __init__(self, token):
        self.token = token

class TokenLiteralDisplay(TokenDisplay):
    def __init__(self, token):
        self.token = token
        self.value = self.convert(token.value)
    
    def call(self, ctx):
        return self.value

class StringDisplay(TokenLiteralDisplay):
    convert = eval

class FloatDisplay(TokenLiteralDisplay):
    convert = float

class IntDisplay(TokenLiteralDisplay):
    convert = int

class NameDisplay(TokenDisplay):
    def call(self, ctx):
        return context_lookup(ctx, self.token.value)

class ListDisplay(AbstractSyntaxTree):
    def __init__(self, token, atoms):
        self.token = token
        self.atoms = atoms
    
    def call(self, ctx):
        return [atom(ctx) for atom in self.atoms]

class Block(AbstractSyntaxTree):
    def __init__(self, token, commands):
        self.token = token
        self.commands = commands
    
    def call(self, ctx):
        last = None
        for command in self.commands:
            last = command(ctx)
        return last

class AttributeDisplay(AbstractSyntaxTree):
    def __init__(self, atom, name):
        self.token = atom.token
        self.atom = atom
        self.name = name
    
    def call(self, ctx):
        return getattr(self.atom(ctx), self.name)

class Command(AbstractSyntaxTree):
    def __init__(self, f, args):
        self.token = f.token
        self.f = f
        self.args = args
    
    def call(self, ctx):
        f = self.f(ctx)
        
        return (
            f(ctx, self.args) if isinstance(f, SpecialForm) else
            f(*[arg(ctx) for arg in self.args]))

class SpecialForm(object):
    def __init__(self, f):
        self.f = f
    
    def __call__(self, ctx, args):
        return self.f(ctx, args)

### context

def context_find(ctx, name):
    while name not in ctx and '__parent__' in ctx:
        ctx = ctx['__parent__']
    return ctx

def context_lookup(ctx, name):
    return context_find(ctx, name)[name]

global_context = {
    'print' : print
}
global_context['__context__'] = global_context

def new_context(parent = global_context):
    context = {'__parent__' : parent}
    context['__context__'] = context
    return context

### repl

def execute(string, context = None, file_name = '<unnamed>'):
    if context is None:
        context = new_context()
    
    return parse(string, file_name)(context)

def run(string):
    try: execute(string)
    except Exception as e:
        print(repr(e))
        for ast in e.ast_stack:
            print('%s: %s' %
                (ast.__class__.__name__,
                    ast.token.location_string()))

def partially_formed(string):
    inners = '([{'
    outers = ')]}'
    depth = 0
    for token in lex(string):
        if token.type in inners:
            depth += 1
        elif token.type in outers:
            depth -= 1
        
        if depth < 0:
            return False
    
    return depth > 0

def repl():
    while True:
        command = input('>>> ')
        while partially_formed(command):
            command += input('... ')
        result = run(command)
        if result is not None:
            print(result)
