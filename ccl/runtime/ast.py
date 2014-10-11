class AbstractSyntaxTree(object):
    pass

class TokenDisplay(AbstractSyntaxTree):
    def __init__(self, token):
        self.token = token

class TokenLiteralDisplay(TokenDisplay):
    def __init__(self, token):
        self.token = token
        self.value = self.convert(token.value)
    
    def __call__(self, scope):
        return self.value

class StringDisplay(TokenLiteralDisplay):
    convert = eval

class FloatDisplay(TokenLiteralDisplay):
    convert = float

class IntDisplay(TokenLiteralDisplay):
    convert = int

class NameDisplay(TokenDisplay):
    def __call__(self, scope):
        from ccl.runtime.corelib import lookup
        return lookup(self, scope, self.token.value)
    
    def __str__(self):
        return self.token.value

class ListDisplay(AbstractSyntaxTree):
    def __init__(self, token, atoms):
        self.token = token
        self.atoms = atoms
    
    def __call__(self, scope):
        return [atom(scope) for atom in self.atoms]
    
    def __iter__(self):
        return iter(self.atoms)

class Block(AbstractSyntaxTree):
    def __init__(self, token, commands):
        self.token = token
        self.commands = commands
    
    def __call__(self, scope):
        last = None
        for command in self.commands:
            last = command(scope)
        return last

class AttributeDisplay(AbstractSyntaxTree):
    def __init__(self, atom, name):
        self.token = atom.token
        self.atom = atom
        self.name = name
    
    def __call__(self, scope):
        from ccl.runtime.corelib import get_attribute
        return get_attribute(self, self.atom(scope), self.name)
    
    def __str__(self):
        return '%s.%s' % (self.atom, self.name)

class Command(AbstractSyntaxTree):
    def __init__(self, f, args):
        self.token = f.token
        self.f = f
        self.args = args
    
    def __call__(self, scope):
        return self.f(scope)(scope, self.args, self)
