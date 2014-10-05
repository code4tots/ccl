"""language.py

ccl's primitive language builtins defined here

"""
from __future__ import print_function

try: input = raw_input
except NameError: pass

from ccl.main import (
    # context
    global_context,
    register,
    context_find,
    
    # ast
    SpecialForm,
    NameDisplay,
    ListDisplay,
    AttributeDisplay)

global_context.update({
    'True'  : True,
    'False' : False,
    'None'  : None,
    
    'print' : print,
    'input' : input,
    'open'  : open,
    
    'list'  : list,
    'tuple' : tuple,
    'dict'  : dict,
    
    'SpecialForm' : SpecialForm,
    })

def assign_values(ctx, lhs, rhs, reassign):
    if isinstance(lhs, NameDisplay):
        if reassign:
            ctx = context_find(ctx)
        
        ctx[str(lhs)] = rhs
        
    elif isinstance(lhs, ListDisplay):
        for sub_lhs, sub_value in zip(lhs, rhs):
            assign_values(ctx, sub_lhs, sub_value, reassign)
    
    else:
        se = SyntaxError('invalid assignment')
        se.ast_stack = []
        raise se

@register('assign')
@SpecialForm
def assign(ctx, args):
    lhs, rhs = args
    rhs = rhs(ctx)
    assign_values(ctx, lhs, rhs, reassign = False)
    return rhs

@register('reassign')
@SpecialForm
def reassign(ctx, args):
    lhs, rhs = args
    rhs = rhs(ctx)
    assign_values(ctx, lhs, rhs, reassign = True)
    return rhs

@register('display')
@SpecialForm
def display(ctx, args):
    arg, = args
    return arg

@register('lambda')
@SpecialForm
def lambda_(ctx, args):
    pass

@register('with')
@SpecialForm
def with_(ctx, args):
    pass