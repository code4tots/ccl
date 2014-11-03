"""This time, completely ignore extensibility.
Dynamically typed. Dynamically scoped.
"""

def parse(string):
    stack = [[]]
    for token in string.split():
        if   token == '[': stack.append([])
        elif token == ']': stack[-2].append(tuple(stack.pop()))
        else:              stack[-1].append(token)
    assert len(stack) == 1, "Mismatched brackets"
    return stack[0]

def execute(thunk, stack, environment):
    if callable(thunk):
        thunk(stack, environment)
    elif isinstance(thunk, str):
        assert len(thunk) > 0, "Empty token"
        c = thunk[0]
        rest = thunk[1:]
        if c.isdigit() or c in '+-' and len(rest) > 1 and rest[0].isdigit():
            stack.append((float if '.' in rest else int)(thunk))
        elif c == ':': stack.append(rest)
        elif c == '$': stack.append(environment[rest])
        elif c == '=': environment[rest] = stack.pop()
        else:          execute(environment[thunk], stack, environment)
    elif isinstance(thunk, tuple):
        stack.append(list(thunk))
    elif isinstance(thunk, list):
        for part in thunk:
            execute(part, stack, environment)
    else:
        raise TypeError(thunk)

model_environment = { '-None' : None }

class Environment(object):
    def __init__(self, model_environment):
        self.tables = [{k:v for k,v in model_environment.items()}]
    
    def push(self):
        self.tables.append(dict())
    
    def pop(self):
        self.tables.pop()
    
    def __contains__(self, key):
        return any(key in table for table in self.tables)
    
    def __getitem__(self, key):
        for table in reversed(self.tables):
            if key in table:
                return table[key]
        raise KeyError(key)
    
    def __setitem__(self, key, value):
        self.tables[-1][key] = value

def register(name):
    def wrapper(function):
        model_environment[name] = function
        return function
    return wrapper

string = r"""

"""

execute(parse(string), [], Environment(model_environment))
