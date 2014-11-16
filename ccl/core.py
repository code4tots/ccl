from importlib import import_module

class Scope(object):
    def __init__(self):
        self.tables = [{
            'python-import': (lambda stack, scope:
                import_module(stack.pop()).init(scope)),
            'import': (lambda stack, scope: (
                lambda file_: file_.__enter__() and 
                    run(file_.read(), stack, scope) and file_.__exit__()))}]
    
    def __getitem__(self, key):
        table = self.tables[-1]
        while key not in table and '__parent__' in table:
            table = table['__parent__']
        return table[key]
    
    def __setitem__(self, key, value):
        self.tables[-1][key] = value
    
    def register(self, f):
        self[f.__name__] = f
    
    # TODO: For now Scope will only support dynamic scoping.
    # However, in the future, push and pop may accept parent arguments
    # so that we may support static typing.
    
    def push(self):
        self.tables.append({'__parent__': self.tables[-1]})
    
    def pop(self):
        self.tables.pop()

def parse(string):
    stack = [[]]
    for token in string.split():
        if   token == '[':
            stack.append([])
        elif token == ']':
            stack[-2].append(stack.pop())
        else:
            try:
                token = int(token)
            except ValueError:
                try:
                    token = float(token)
                except ValueError:
                    pass
            stack[-1].append(token)
    assert len(stack) == 1, "Missing close brackets"
    return stack[0]

def execute(thunk, stack, scope):
    if isinstance(thunk, (list,int,float)):
        stack.append(thunk)
    elif isinstance(thunk, str):
        if thunk.startswith(':'):
            stack.append(thunk[1:])
        elif thunk.startswith('='):
            scope[thunk[1:]] = stack.pop()
        elif thunk.startswith('$'):
            stack.append(scope[thunk[1:]])
        else:
            summon(scope[thunk], stack, scope)
    else:
        raise Exception(thunk)

def summon(thunk, stack, scope):
    if isinstance(thunk, list):
        for item in thunk:
            execute(item, stack, scope)
    else:
        thunk(stack, scope)

def run(string, stack, scope):
    summon(parse(string), stack or [], scope or Scope())
