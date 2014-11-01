"""This time, completely ignore extensibility.

Just make it a language I would want to use for fun.

MAKE IT FUN.

What if the language was regular-expression-esq?

"Write only" language perlier than perl.

A very terse forth-like language.

[ p p + ] =f =g
1 2 f

{1 2 3}

"""

def parse(string):
    tokens = string.split()
    stack = [ [] ]
    for token in tokens:
        if token == '[':
            stack.append([])
        elif token == ']':
            stack[-2].append(tuple(stack.pop()))
        else:
            stack[-1].append(token)
    assert len(stack) == 1, "Mismatched parenthesis"
    return stack[0]

def execute(thunk, environment=None, stack=None):
    if environment is None:
        environment = dict()

    if stack is None:
        stack = []

    if isinstance(thunk, str):
        if thunk.startswith('='):
            name = thunk[1:]
            environment[name] = stack.pop()
        elif thunk.startswith('$'):
            name = thunk[1:]
            stack.append(environment[name])
        elif thunk.startswith(':'):
            value = thunk[1:]
            stack.append(value)
        elif any(d.isdigit() for d in thunk) and all(d.isdigit() or d in '+-' for d in thunk):
            stack.append(int(thunk))
        elif any(d.isdigit() for d in thunk) and all(d.isdigit() or d in '+-.' for d in thunk):
            stack.append(float(thunk))
        else:
            execute(environment[thunk], environment, stack)
    elif isinstance(thunk, tuple):
        stack.append(list(thunk))
    elif isinstance(thunk, list):
        for subthunk in thunk:
            execute(subthunk, environment, stack)
    elif callable(thunk):
        thunk(environment, stack)
    else:
        raise Exception()

string = """

2 5 + @
[ * + ] =f
3 2 1 f @
:hello_world @


:Da_Stack @

[ Comments are here ] #

    1 . :a , .
    2 . :b , ,
    3 . :c , ,
    ## @

5 . 6 , 7 , 8 , 9 , @

#s @


"""

environment = dict()
stack = list()

def register(name):
    def wrapper(f):
        environment[name] = f
    return wrapper

@register('+')
def add(environment, stack): stack[-2] += stack[-1]; stack.pop()
@register('-')
def subtract(environment, stack): stack[-2] -= stack[-1]; stack.pop()
@register('*')
def multiply(environment, stack): stack[-2] *= stack[-1]; stack.pop()
@register('/')
def divide(environment, stack): stack[-2] /= stack[-1]; stack.pop()
@register('#')
def comment(environment, stack): stack.pop()
@register('-p')
def print_(environment, stack): print(stack.pop())
@register('-s')
def s(environment, stack): stack.append(stack)
@register('-e')
def execute_(environment, stack): execute(stack.pop(), environment, stack)
@register(',')
def append(environment, stack): stack[-2].append(stack[-1]); stack.pop()
@register('.')
def singleton(environment, stack): stack.append([stack.pop()])
@register('-d')
def dict_(environment, stack): stack.append(dict(stack.pop()))


execute(parse(string), environment, stack)
