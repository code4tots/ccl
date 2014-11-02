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

model_environment = dict()

def new_environment():
    return {k:v for k,v in model_environment.items()}

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

@register('-pop-stack')
def pop_stack(stack, environment): stack.pop()
@register('-push-environment')
def push_environment(stack, environment): environment.push()
@register('-pop-environment')
def pop_environment(stack, environment): environment.pop()
@register('-equal')
def equal(stack, environment): stack.append(stack.pop() == stack.pop())
@register('-less-than')
def less_than(stack, environment): stack.append(stack.pop() > stack.pop())
@register('-add')
def add(stack, environment): stack[-2] += stack.pop()
@register('-subtract')
def subtract(stack, environment): stack[-2] -= stack.pop()
@register('-multiply')
def multiply(stack, environment): stack[-2] *= stack.pop()
@register('-divide')
def divide(stack, environment): stack[-2] /= stack.pop()
@register('-duplicate')
def duplicate(stack, environment): stack.extend(stack[-stack.pop():])
@register('-stack')
def stack(stack, environment): stack.append(stack)
@register('-print')
def print_(stack, environment): print(stack.pop())
@register('-execute')
def execute_(stack, environment): execute(stack.pop(), stack, environment)


string = """
[ aliases ] -pop-stack

    [ language ] -pop-stack
        $-push-environment =(
        $-pop-environment =)
        $-pop-stack =#
        $-duplicate =-dupn
        [ 2 -duplicate ] =-dup
        [ ( =second =first $second $first ) ] =-swap
        [ ( =n =thunk $n  ) ] =-repeat

    [ arithmetic operations ] #
        $-add =+
        $-subtract =-
        $-multiply =*
        $-divide =/

    [ debugging ] #
        [ Hmm. Do I need anything here? ] #

[ :thunk_evaluation -print ] -execute

-stack -print

:hello_world -print

(
    12 =f
    $f -print
)


1 2
-stack -print

-swap
-stack -print

"""

execute(parse(string), [], Environment(model_environment))
