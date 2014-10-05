"""
The most fundamental tools for the language
"""
from __future__ import print_function
from functools import wraps

from ccl.scope import global_scope, find
from ccl.ast import NameDisplay, ListDisplay, AttributeDisplay
import ccl.exception as ex

def function(wrapped):
    @wraps(wrapped)
    def wrapper(scope, args, ast):
        args = [arg(scope) for arg in args]
        try:
            return wrapped(*args)
        except ex.CclException as e:
            e.callstack.append(ast)
    return wrapper

def register(name):
    def wrapper(f):
        global_scope[name] = f
        return f
    return wrapper

global_scope.update({
    'None'  : None,
    'True'  : True,
    'False' : False,
    })

global_scope.update({
    name : function(f)
    for name, f in {
        'print' : print,
    }.items()})

def assign(scope, lhs, rhs, reassign):
    if isinstance(lhs, NameDisplay):
        lhs = lhs.token.value
        
        if reassign:
            ctx = find(scope, lhs)
        
        scope[lhs] = rhs
    
    elif isinstance(lhs, ListDisplay):
        for element, value in zip(lhs, rhs):
            assign(scope, element, value, reassign)
    
    elif isinstance(lhs, AttributeDisplay):
        atom = lhs.atom(scope)
        attribute = lhs.name
        setattr(atom, attribute, rhs)
    
    else:
        raise ex.RuntimException('invalid assignment')

@register('=')
def assign_macro(scope, args, ast):
    try:
        lhs, rhs = args
    except ValueError:
        raise ex.WrongNumberOfArguments(ast, expected=2, got=len(args))
    rhs = rhs(scope)
    
    assign(scope, lhs, rhs, reassign = False)

@register('=>')
def reassign_macro(scope, args, ast):
    try:
        lhs, rhs = args
    except ValueError:
        raise ex.WrongNumberOfArguments(ast, expected=2, got=len(args))
    rhs = rhs(scope)
    
    assign(scope, lhs, rhs, reassign = True)
