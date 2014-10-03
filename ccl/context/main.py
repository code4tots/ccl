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
    
    'len'     : len,
    'range'   : range,
    
    'list'    : list,
    'tuple'   : tuple,
    'dict'    : dict,
    
    # basic system interface
    'print'   : print,
    'open'    : open,
    'cwd'     : os.getcwd,
    'ls'      :
        # In python 2.x os.listdir does not have default path
        (lambda p=None: os.listdir(os.getcwd() if p is None else p)),
    'cd'      : os.chdir,
    'mkdir'   : os.makedirs,
    'exists'  : os.path.exists,
    'isfile'  : os.path.isfile,
    'islink'  : os.path.islink,
    'isdir'   : os.path.isdir,
    'ismount' : os.path.ismount,
}

global_context['__context__'] = global_context

def new_context(parent = global_context):
    context = {'__parent__' : parent}
    context['__context__'] = context
    return context
