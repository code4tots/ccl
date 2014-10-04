"""Core language stuff.
"""
from ccl.context.main import register, SpecialForm

@register('comment')
@SpecialForm
def comment(ctx, args):
    return args

@register('assign')
@SpecialForm
def assign(ctx, args):
    name, value = args
    value = value(ctx)
    ctx[name.string] = value
    return value

@register('reassign')
@SpecialForm
def reassign(ctx, args):
    name, value = args
    value = value(ctx)
    name.find(ctx)[name.string] = value
    return value

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

@register('def')
@SpecialForm
def def_(ctx, args):
    from ccl.context import new_context
    
    function_name = args[0].string
    arg_names = [x.string for x in args[1:-1]]
    body = args[-1]
    
    def f(*args):
        fctx = new_context(ctx)
        for name, value in zip(arg_names, args):
            fctx[name] = value
        
        for name in arg_names:
            if name not in fctx:
                fctx[name] = None
        
        return body(fctx)
    
    ctx[function_name] = f
    f.__qualname__ = f.__name__ = function_name
    
    return f

@register('class')
@SpecialForm
def class_(ctx, args):
    from ccl.context import new_context
    
    if len(args) == 2:
        name, body = args
        bases = ()
    else:
        name, bases, body = args
    
    name = name.string
    bases = tuple(base(ctx) for base in bases)
    
    dict_ = new_context(ctx)
    body(dict_)
    
    cls = type(name, bases, dict_)
    
    ctx[name] = cls
    
    return cls
