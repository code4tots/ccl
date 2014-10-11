"""Core values that are required for runtime.
"""
### Rename Python objects
PythonBaseException = BaseException
PythonException = Exception

### Scope

global_scope = dict()
global_scope['__global__'] = global_scope
global_scope['__stack_trace__'] = []

def new_scope(parent):
    scope = dict()
    scope['__global__'] = parent['__global__']
    scope['__parent__'] = parent

### Fundamental Classes

class Object(object):
    pass

class BaseException(Object, PythonBaseException):
    pass

class Exception(PythonException):
    def __init__(self, message, call_stack):
        self.message = message
        self.call_stack = call_stack

class Number(Object):
    @staticmethod
    def from_python_number(value):
        return (Int if isinstance(value, int) else Float)(value)
    
    def __init__(self, value):
        self.value = value

class Int(Number):
    pass

class Float(Number):
    pass

class String(Object):
    pass
