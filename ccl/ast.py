class Ast(object):
    pass

class Literal(Ast):
    def __init__(self, string):
        self.value = self.convert(string)
    
    def __call__(self, ctx):
        return self.value

class Int(Literal):
    convert = int

class Float(Literal):
    convert = float

class String(Literal):
    convert = eval

class Name(Ast):
    def __init__(self, string):
        self.string = string
    
    def find(self, ctx):
        name = self.string
        while name not in ctx and '__parent__' in ctx:
            ctx = ctx['__parent__']
        return ctx
    
    def __call__(self, ctx):
        return self.find(ctx)[self.string]

class Attribute(Ast):
    def __init__(self, atom, name):
        self.atom = atom
        self.name = name
    
    def __call__(self, ctx):
        return getattr(self.atom(ctx), self.name)

class List(Ast):
    def __init__(self, atoms):
        self.atoms = atoms
    
    def __call__(self, ctx):
        return [atom(ctx) for atom in self.atoms]

class Command(Ast):
    def __init__(self, f, args):
        self.f = f
        self.args = args
    
    def __call__(self, ctx):
        from ccl.context import SpecialForm
        
        f = self.f(ctx)
        
        if isinstance(f,SpecialForm):
            return f(ctx, self.args)
        
        else:
            args = [arg(ctx) for arg in self.args]
            return f(*args)

class Block(Ast):
    def __init__(self, commands):
        self.commands = commands
    
    def __call__(self, ctx):
        last = None
        for command in self.commands:
            last = command(ctx)
        return last
