"""This time, completely ignore extensibility.

Just make it a language I would want to use for fun.

MAKE IT FUN.

What if the language was regular-expression-esq?

A very terse forth-like language.

( p p + ) =f 1 2 $f

( [ p p + ] =f ) =g
1 2 f

{1 2 3}

"""

def parse(string):
    tokens = string.split()
    stack = [ [] ]
    for token in tokens:
        if token in ('(', '['):
            stack.append([])
        elif token == ')':
            stack[-2].append(list(stack.pop()))
        elif token == ']':
            stack[-2].append(tuple(stack.pop()))
        else:
            stack[-1].append(token)
    if len(stack) != 1:
        raise Exception()
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
        elif all(d.isdigit() or d in '+-' for d in thunk):
            stack.append(int(thunk))
        elif all(d.isdigit() or d in '+-.' for d in thunk):
            stack.append(float(thunk))
        else:
            execute(environment[thunk], environment, stack)
    elif isinstance(thunk, tuple):
        stack.append(list(thunk))
    elif isinstance(thunk, list):
        for subthunk in thunk:
            execute(subthunk, environment, stack)
    else:
        raise Exception()

string = """
[ 2 ] =f f f
5 =g $g
"""

environment = dict()
stack = list()

execute(parse(string), environment, stack)
print(stack)
