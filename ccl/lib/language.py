"""
The most fundamental language constructs
"""
from __future__ import print_function

from ccl.scope import global_scope, find, new_scope, function, register
from ccl.ast import NameDisplay, ListDisplay, AttributeDisplay
import ccl.exception as ex

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

@register('#')
def comment(scope, args, ast):
    pass

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
    
    return rhs

@register('=>')
def reassign_macro(scope, args, ast):
    try:
        lhs, rhs = args
    except ValueError:
        raise ex.WrongNumberOfArguments(ast, expected=2, got=len(args))
    rhs = rhs(scope)
    
    assign(scope, lhs, rhs, reassign = True)
    
    return rhs

@register('\\\\')
def macro(scope, args, ast):
    if len(args) != 3:
        raise ex.WrongNumberOfArguments(ast, expected=3, got=len(args))
    
    names = args[:-1]
    body = args[-1]
    
    def macro_function(*args):
        mscope = new_scope(scope)
        for name, arg in zip(names, args):
            mscope[name] = arg
        return body(mscope)
    
    return macro_function
    
@register('\\')
def lambda_(scope, args, ast):
    body  = args[-1]
    if not all(isinstance(arg, NameDisplay) for arg in args[:-1]):
        raise ex.RuntimException(
            ast,
            'all arguments except the last must be names')
    names = [arg.token.value for arg in args[:-1]]
    
    @function
    def lambda_function(*args):
        fscope = new_scope(scope)
        fscope['__args__'] = args
        for name, arg in zip(names, args):
            fscope[name] = arg
        for name in names:
            if name not in fscope:
                fscope[name] = None
        return body(fscope)
    
    return lambda_function
