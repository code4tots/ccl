from __future__ import print_function
import os
from ccl.runtime import SpecialForm

builtin_scope = dict()

def new_scope(parent):
    scope = {'__parent__' : parent}
    scope.update({
        '__global__' : parent['__global__'],
        '__scope__'  : scope})
    return scope

builtin_scope.update({
    '__global__' : builtin_scope,
    '__scope__' : builtin_scope,
    '__call_stack__' : [],
    '__import_table__' : dict(),
    
    'getattr' : getattr,
    'len' : len,
    'print' : print})

def register(name):
    def register_(function):
        if isinstance(function, SpecialForm):
            function.name = name
        builtin_scope[name] = function
        return function
    return register_

@register('import')
@SpecialForm
def import_(scope, args):
    import os
    from ccl.runtime import run_string, load_module
    path_display, = args
    path = path_display(scope)
    realpath = os.path.realpath(path)
    import_table = scope['__global__']['__import_table__']
    
    if realpath not in import_table:
        import_table[realpath] = load_module(realpath, scope['__global__'])
    
    return import_table[realpath]

@register('print-exception-message')
def print_exception_message(exception, call_stack):
    print("**** UNCAUGHT EXCEPTION **** ")
    print(str(type(exception)) + '\n' + str(exception))
    for display in call_stack:
        print(display.location_string)

@register('let')
@SpecialForm
def let(scope, args):
    """Define and assign a value to the current scope.
    """
    name_display, value_display = args
    scope[name_display.name] = value = value_display(scope)
    return value

@register('let-')
@SpecialForm
def let_(scope, args):
    """Redefine a value that has already been defined.
    """
    name_display, value_display = args
    name = name_display.name
    name_display.find(scope)[name] = value = value_display(scope)
    return value

