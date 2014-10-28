"""This time, completely ignore extensibility.

Just make it a language I would want to use for fun.

MAKE IT FUN.

What if the language was regular-expression-esq?

A very terse forth-like language.

( p p + ) =f 1 2 $f

( [ p p + ] =f ) =g
1 2 f

"""

def parse(string):
    tokens = string.split()
    stack = [ [] ]
    for token in tokens:
        if token in ('(', '['):
            stack.append([])
        elif token == ')':
            stack[-2].append(tuple(stack.pop()))
        elif token == ']':
            stack[-2].append(list(stack.pop()))
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
            name = thunk[1:]
            execute(environment[name], environment, stack)
    elif isinstance(thunk, list):
        stack.append(tuple(thunk))
    elif isinstance(thunk, tuple):
        for subthunk in thunk:
            execute(subthunk, environment, stack)
    else:
        raise Exception()
