"""
"""
class Context(object):
    def __init__(self, table, stack=None, depth=0):
        self.table = table
        self.stack = stack or []
        self.depth = depth
    
    def __getitem__(self, key):
        return self.table[key]

def execute(thunk, context):
    if thunk == '[':
        context.depth += 1
        context.stack.append([])
    elif thunk == ']':
        context.depth -= 1
        context.stack[-2].append(context.stack.pop())
    elif isinstance(thunk, str) and not context.depth:
        if thunk[0] == '$':
            context.stack.append(context[thunk[1:]])
        else:
            context[thunk](context)
    else:
        context.stack.append(thunk)

def run(string, context):
    for thunk in string.split():
        execute(thunk, context)
