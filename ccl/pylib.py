from __future__ import print_function
from ccl.runtime import SpecialForm

builtin_scope = dict()

builtin_scope.update({
    '__global__' : builtin_scope,
    '__scope__' : builtin_scope,
    
    'getattr' : getattr,
    'print' : print})

def register(name):
    def register_(function):
        builtin_scope[name] = function
        return function
    return register_

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

