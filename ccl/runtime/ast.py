import ccl.runtime.corelib as cl

class AbstractSyntaxTree(cl.Object):
    def __init__(self, cst):
        self.cst = cst

class ConstantDisplay(AbstractSyntaxTree):
    def __init__(self, cst, value):
        super(ConstantDisplay, self).__init__(cst)
        self.value = value
    
    def __call__(self, scope):
        return self.value

class Block(AbstractSyntaxTree):
    def __init__(self, cst, commands):
        super(Block, self).__init__(cst)
        self.commands = commands
    
    def __call__(self, scope):
        last = cl.none
        for command in self.commands:
            last = command(scope)
        return last

class Command(AbstractSyntaxTree):
    def __init__(self, cst, f, args):
        super(Command, self).__init__(cst)
        self.f = f
        self.args = args
    
    def __call__(self, scope):
        return self.f(self, scope, self.args)
