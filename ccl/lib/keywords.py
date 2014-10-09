"""Implementation of macros that are traditionally Python keywords
"""

from ccl.scope import register
from ccl.ast import SpecialForm
import ccl.exception as ex

@register('and')
@SpecialForm
def and_(scope, args, ast):
    if len(args) != 2:
        raise ex.WrongNumberOfArguments(ast, expected=2, got=len(args))
    
    lhs, rhs = args
    lhs = lhs(scope)
    return rhs(scope) if lhs else lhs

@register('or')
@SpecialForm
def or_(scope, args, ast):
    if len(args) != 2:
        raise ex.WrongNumberOfArguments(ast, expected=2, got=len(args))
    
    lhs, rhs = args
    lhs = lhs(scope)
    return lhs if lhs else rhs(scope)

@register('return')
@SpecialForm
def return_(scope, args, ast):
    if len(args) != 1:
        raise ex.WrongNumberOfArguments(ast, expected=1, got=len(args))
    
    return_value = args[0](scope)
    
    raise ex.ReturnException(ast, return_value)

@register('while')
@SpecialForm
def while_(scope, args, ast):
    if len(args) != 2:
        raise ex.WrongNumberOfArguments(ast, expected=2, got=len(args))
    
    condition, body = args
    last = None
    
    try:
        while condition(scope):
            last = body(scope)
    except ex.BreakException:
        pass
    
    return last

@register('break')
@SpecialForm
def break_(scope, args, ast):
    if len(args) != 0:
        raise ex.WrongNumberOfArguments(ast, expected=0, got=len(args))
    
    raise ex.BreakException(ast)
