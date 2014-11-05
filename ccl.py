"""Fun to use and easy to implement programming language."""
import os
import sys

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
            summon(scope[thunk], stack, scope)
    else:
        raise Exception(thunk)

def summon(thunk, stack, scope):
    if isinstance(thunk, list):
        for item in thunk:
            execute(item, stack, scope)
    else:
        thunk(stack, scope)

def run(string, stack, scope):
    summon(parse(string), stack, scope)

scope = dict()

def register(f):
    scope[f.__name__] = f
    return f

@register
def __print(stack, scope):
    print(stack.pop())

@register
def __read(stack, scope):
    stack.append(sys.stdin.readline())

@register
def __stack(stack, scope):
    stack.append(stack)

@register
def __map(stack, scope):
    f = stack.pop()
    items = stack.pop()
    results = []
    for item in items:
        results.append(item)
        summon(f, results, scope)
    stack.append(results)

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
def __space(stack, scope):
    stack.append(' ')

@register
def __join(stack, scope):
    separator = stack.pop()
    strings = stack.pop()
    stack.append(separator.join(strings))

@register
def __strip(stack, scope):
    stack[-1] = stack[-1].strip()

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
$__read =r
$__stack =s
$__map =map
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
$__space =\s
$__join =j
$__strip =strip
[ r strip ] =rs
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

[
    rs =Message
    :you \s + :typed: + \s + $Message + p
    :you . :typed , $Message , \s j p
] =

1 . 2 , 3 , [ 1 + ] map p

"""

run(cclrc, [], scope)
