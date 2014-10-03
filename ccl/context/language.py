"""Core language stuff.
"""
from ccl.context.main import register, SpecialForm

@register('if')
@SpecialForm
def if_(ctx, args):
    if len(args) == 2:
        condition, if_block = args
        from ccl.ast import Block
        else_block = Block(())
    else:
        condition, if_block, else_block = args
    
    return if_block(ctx) if condition(ctx) else else_block(ctx)

@register('while')
@SpecialForm
def while_(ctx, args):
    condition, block = args
    last = None
    while condition(ctx):
        last = block(ctx)
    return last
