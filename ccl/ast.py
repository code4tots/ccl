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
        from ccl.scope import lookup
        try:
            return lookup(scope, self.token.value)
        except KeyError:
            import ccl.exception as ex
            e = ex.KeyError(self.token.value)
            e.callstack.append(self)
            raise e

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
        import ccl.exception as ex
        
        value = self.atom(scope)
        try:
            return getattr(self.atom(scope), self.name)
        except AttributeError:
            e = ex.AttributeError(value, self.name)
            e.callstack.append(self)
            raise e

class Command(AbstractSyntaxTree):
    def __init__(self, f, args):
        self.token = f.token
        self.f = f
        self.args = args
    
    def __call__(self, scope):
        import ccl.exception as ex
        
        f = self.f(scope)
        
        try:
            return f(scope, self.args)
        except ex.RuntimeException as e:
            e.callstack.append(self)
            raise
        except ValueError:
            e = ex.RuntimeException('wrong number of arguments')
            e.callstack.append(self)
            raise e