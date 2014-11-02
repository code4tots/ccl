"""This time, completely ignore extensibility.

JUST MAKE IT FUN.

What if the language was regular-expression-esq?

"Write only" language perlier than perl.

A very terse forth-like language.

A very EVIL langauge. It treats you like an adult.

[ p p + ] =f =g
1 2 f

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
    if isinstance(thunk, str):
        assert len(thunk) > 0, "Empty token"
        c = thunk[0]
        rest = thunk[1:]
        if c.isdigit() or c in '+-' and len(rest) > 1 and rest[0].isdigit():
            stack.append((float if '.' in rest else int)(thunk))
        elif c == ':': stack.append(rest)
        elif c == '$': stack.append(environment[rest])
        elif c == '=': environment[rest] = stack.pop()
        else:          environment[thunk](stack, environment)
    elif isinstance(thunk, tuple):
        stack.append(list(thunk))
    elif isinstance(thunk, list):
        for part in thunk:
            execute(part, stack, environment)

model_environment = dict()

def new_environment():
    return {k:v for k,v in model_environment.items()}

def register(name):
    def wrapper(function):
        model_environment[name] = function
        return function
    return wrapper

@register('-pop-stack')
def pop_stack(stack, environment): stack.pop()
@register('-push-environment')
def push_environment(stack, environment): 
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
        $-duplicate =++
        [ 2 -duplicate ] =+++
        [ ] =-repeat

    [ arithmetic operations ] #
        $-add =+
        $-subtract =-
        $-multiply =*
        $-divide =/

    [ debugging ] #
        $-print =p

[ :thunk_evaluation -print ] -execute

-stack -print

:hello_world -print

"""

execute(parse(string), [], new_environment())
