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

@register('if')
@SpecialForm
def if_(scope, args, ast):
    if len(args) not in (2, 3):
        raise ex.WrongNumberOfArguments(ast, expected=(2,3), got=len(args))
    
    if len(args) == 2:
        condition, ifbody = args
        elsebody = None
    
    else:
        condition, ifbody, elsebody = args
    
    if condition(scope):
        return ifbody(scope)
    elif elsebody is not None:
        return elsebody(scope)

@register('try')
@SpecialForm
def try_(scope, args, ast):
    if len(args) != 4:
        raise ex.WrongNumberOfArguments(ast, expected=4, got=len(args))
    
    tryblock, etype, ename, elseblock = args
    
    etype = etype(scope)
    ename = str(ename)
    
    try:
        return tryblock(scope)
    except etype as e:
        scope[ename] = e
        return elseblock(scope)
