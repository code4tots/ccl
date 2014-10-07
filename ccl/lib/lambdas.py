"""lambda and macro
"""
from ccl.scope import register, new_scope
from ccl.ast import SpecialForm, NameDisplay
import ccl.exception as ex

@register('\\\\')
@SpecialForm
def macro(scope, args, ast):
    if len(args) != 3:
        raise ex.WrongNumberOfArguments(ast, expected=3, got=len(args))
    
    if not all(isinstance(arg, NameDisplay) for arg in args[:-1]):
        raise ex.RuntimeException(
            ast,
            'all arguments except the last must be names')
    
    body = args[-1]
    names = [arg.token.value for arg in args[:-1]]
    
    @SpecialForm
    def macro_function(*args):
        mscope = new_scope(scope)
        for name, arg in zip(names, args):
            mscope[name] = arg
        try:
            return body(mscope)
        except ex.ReturnException as e:
            return e.return_value
    
    return macro_function

@register('\\')
@SpecialForm
def lambda_(scope, args, ast):
    if not all(isinstance(arg, NameDisplay) for arg in args[:-1]):
        raise ex.RuntimeException(
            ast,
            'all arguments except the last must be names')
    names = [arg.token.value for arg in args[:-1]]
    body  = args[-1]
    
    def lambda_function(*args):
        fscope = new_scope(scope)
        fscope['__args__'] = args
        for name, arg in zip(names, args):
            fscope[name] = arg
        for name in names:
            if name not in fscope:
                fscope[name] = None
        try:
            return body(fscope)
        except ex.ReturnException as e:
            return e.return_value
    lambda_function.name = 'lambda_function'
    
    return lambda_function

