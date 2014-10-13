builtin_scope = dict()

builtin_scope['__global__'] = builtin_scope

def register(name):
    def register_(function):
        

def let(scope, args):
    """Define and assign a value to the current scope.
    """
    name_display, value_display = args
    scope[name_display.name] = value = value_display(scope)
    return value

def let_(scope, args):
    """Redefine a value that has already been defined.
    """
    name_display, value_display = args
    name = name_display.name
    name_display.find(scope)[name] = value = value_display(scope)
    return value
