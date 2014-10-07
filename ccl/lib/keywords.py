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

