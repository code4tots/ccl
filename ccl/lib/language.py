"""
The most fundamental tools for the language
"""
from __future__ import print_function
from ccl.scope import global_scope

def function(wrapped):
    from functools import wraps
    @wraps(wrapped)
    def wrapper(ctx, args):
        return wrapped(*[arg(ctx) for arg in args])
    return wrapper

def register(name):
    def wrapper(f):
        global_scope[name] = f
        return f
    return wrapper

global_scope.update({
    name : function(f)
    for name, f in {
        'print' : print,
    }.items()})

def assign(ctx, lhs, rhs, reassign):
    from ccl.scope import find
    from ccl.ast import NameDisplay, ListDisplay
    
    if isinstance(lhs, NameDisplay):
        lhs = lhs.token.value
        
        if reassign:
            ctx = find(ctx, lhs)
        
        ctx[lhs] = rhs
    
    elif isinstance(lhs, ListDisplay):
        for element, value in zip(lhs, rhs):
            assign(ctx, element, value, reassign)
    
    else:
        import ccl.exception as ex
        raise ex.RuntimException('invalid assignment')

@register('=')
def assign_macro(ctx, args):
    lhs, rhs = args
    rhs = rhs(ctx)
    
    assign(ctx, lhs, rhs, reassign = False)

@register('=>')
def reassign_macro(ctx, args):
    lhs, rhs = args
    rhs = rhs(ctx)
    
    assign(ctx, lhs, rhs, reassign = True)
