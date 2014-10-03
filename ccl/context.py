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
    'print' : print
}

def new_context(parent=global_context):
    return {'__parent__' : global_context}


