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
    summon(parse(string), stack, scope)
