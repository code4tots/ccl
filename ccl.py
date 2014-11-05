"""Fun to use and easy to implement programming language."""
import os

try:                from   urllib import request
except ImportError: import urllib2 as    request

def parse(string):
    stack = [[]]
    for token in string.split():
        if   token == '[':
            stack.append([])
        elif token == ']':
            stack[-2].append(stack.pop())
        else:
            try:
                token = int(token)
            except ValueError:
                try:
                    token = float(token)
                except ValueError:
                    pass
            stack[-1].append(token)
    assert len(stack) == 1, "Missing close brackets"
    return stack[0]

def execute(thunk, stack, scope):
    if isinstance(thunk, (list,int,float)):
        stack.append(thunk)
    elif isinstance(thunk, str):
        if thunk.startswith(':'):
            stack.append(thunk[1:])
        elif thunk.startswith('='):
            scope[thunk[1:]] = stack.pop()
        elif thunk.startswith('$'):
            stack.append(scope[thunk[1:]])
        else:
            value = scope[thunk]
            if isinstance(value, list):
                for item in value:
                    execute(item, stack, scope)
            else:
                value(stack, scope)
    else:
        raise Exception(thunk)

def run(string, stack, scope):
    for thunk in parse(string):
        execute(thunk, stack, scope)

scope = dict()

def register(f):
    scope[f.__name__] = f
    return f

@register
def __print(stack, scope):
    print(stack.pop())

@register
def __stack(stack, scope):
    stack.append(stack)

@register
def __add(stack, scope):
    stack[-2] += stack[-1]; stack.pop()

@register
def __subtract(stack, scope):
    stack[-2] -= stack[-1]; stack.pop()

@register
def __multiply(stack, scope):
    stack[-2] += stack[-1]; stack.pop()

@register
def __divide(stack, scope):
    stack[-2] /= stack[-1]; stack.pop()

@register
def __singleton(stack, scope):
    stack.append([stack.pop()])

@register
def __append(stack, scope):
    stack[-2].append(stack[-1]); stack.pop()

@register
def __cwd(stack, scope):
    stack.append(os.getcwd())

@register
def __ls(stack, scope):
    stack.append(os.listdir(os.getcwd()))

@register
def __ls_(stack, scope):
    stack.append(os.listdir(stack.pop()))

@register
def __cd(stack, scope):
    os.chdir(stack.pop())

@register
def __http_get(stack, scope):
    try:
        f = request.urlopen(stack.pop())
    except Exception as e:
        stack.append(e)
        return
    
    try:
        stack.append(f.read())
    except Exception as e:
        stack.append(e)
    finally:
        f.close()



cclrc = """
[ Comments here !!! ] =

$__print =p
$__stack =s
$__add =+
$__subtract =-
$__multiply =*
$__divide =/
$__singleton =.
$__append =,
$__cwd =cwd
$__ls =ls
$__ls_ =ls-
$__cd =cd
$__http_get =http-get

1 2 + p
5 . 6 , 7 , p
:hello . :world , p

cwd ls- p
ls p

:.. cd cwd p ls p

[ :http://www.google.com http-get ] =

s p

[ :http://en.wikipedia.org/w/api.php?format=json&action=query&titles=Main%20Page&prop=revisions&rvprop=content http-get ] =

"""

run(cclrc, [], scope)
