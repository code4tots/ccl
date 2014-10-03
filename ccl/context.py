from __future__ import print_function
import os

class SpecialForm(object):
    def __init__(self, f):
        self.f = f
    
    def __call__(self, ctx, args):
        return self.f(ctx, args)

def register(name):
    def wrapper(f):
        global_context[name] = f
        return f
    return wrapper

global_context = {
    # language
    'just'    : (lambda x : x),
    'None'    : None,
    'True'    : True,
    'False'   : False,
    
    # basic system interface
    'print'   : print,
    'cwd'     : os.getcwd,
    'ls'      : os.listdir,
    'cd'      : os.chdir,
    'mkdir'   : os.makedirs,
    'exists'  : os.path.exists,
    'isfile'  : os.path.isfile,
    'islink'  : os.path.islink,
    'isdir'   : os.path.isdir,
    'ismount' : os.path.ismount 
}

def new_context(parent = global_context):
    return {'__parent__' : global_context}

# language

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

