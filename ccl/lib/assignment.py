from ccl.scope import find, register
from ccl.ast import SpecialForm, NameDisplay, ListDisplay, AttributeDisplay
import ccl.exception as ex

def assign(scope, lhs, rhs, reassign):
    if isinstance(lhs, NameDisplay):
        lhs = lhs.token.value
        
        if reassign:
            ctx = find(scope, lhs)
        
        if isinstance(rhs,SpecialForm) and rhs.name is None:
            rhs.name = lhs
        
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
@SpecialForm
def assign_macro(scope, args, ast):
    try:
        lhs, rhs = args
    except ValueError:
        raise ex.WrongNumberOfArguments(ast, expected=2, got=len(args))
    rhs = rhs(scope)
    
    assign(scope, lhs, rhs, reassign = False)
    
    return rhs

@register('=>')
@SpecialForm
def reassign_macro(scope, args, ast):
    try:
        lhs, rhs = args
    except ValueError:
        raise ex.WrongNumberOfArguments(ast, expected=2, got=len(args))
    rhs = rhs(scope)
    
    assign(scope, lhs, rhs, reassign = True)
    
    return rhs
