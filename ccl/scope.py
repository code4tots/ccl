global_scope = dict()
global_scope['__scope__'] = global_scope
global_scope['__global__'] = global_scope

def find(scope, name):
    while name not in scope:
        scope = scope['__parent__']
    return scope
    
def lookup(scope, name):
    return find(scope, name)[name]

def new_scope(parent):
    scope = {'__parent__' : global_scope}
    scope['__scope__'] = scope
    scope['__global__'] = global_scope['__global__']
    return scope

def register(name):
    def register_(f):
        global_scope[name] = f
    return register_
