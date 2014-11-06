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
def __stack(stack, scope):
    stack.append(stack)

@register
def __singleton(stack, scope):
    stack.append([stack.pop()])

@register
def __append(stack, scope):
    stack[-2].append(stack[-1]); stack.pop()

@register
def __add(stack, scope):
    stack[-2] += stack[-1]; stack.pop()

@register
def __subtract(stack, scope):
    stack[-2] -= stack[-1]; stack.pop()

@register
def __multiply(stack, scope):
    stack[-2] *= stack[-1]; stack.pop()

@register
def __divide(stack, scope):
    stack[-2] /= stack[-1]; stack.pop()

@register
def __space(stack, scope):
    stack.append(' ')

@register
def __strip(stack, scope):
    stack.append(stack.pop().strip())

@register
def __join(stack, scope):
    separator = stack.pop()
    strings = stack.pop()
    stack.append(separator.join(strings))

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
def __print(stack, scope):
    print(stack.pop())

@register
def __read(stack, scope):
    stack.append(sys.stdin.readline())

@register
def __cwd(stack, scope):
    stack.append(os.getcwd())

@register
def __ls_(stack, scope):
    stack.append(os.listdir(stack.pop()))

@register
def __cd(stack, scope):
    os.chdir(stack.pop())

@register
def __open(stack, scope):
    # TODO: Crossplatform. On Windows
    # You can use os.startfile.
    os.system("open " + stack.pop())

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
[ language ] =
    $__stack =s
    $__singleton =.
    $__append =,
    $__add =+
    $__subtract =-
    $__multiply =*
    $__divide =/
    $__space =\s
    $__strip =strip
    $__join =join
    $__map =map

[ file io ] =
    $__print =p
    $__read =read
    [ read strip ] =rs
    $__cwd =cwd
    $__ls_ =ls-
    [ cwd ls- ] =ls
    $__cd =cd
    $__open =open

[ internet ] =
    $__http_get =http-get

s p
1 . 2 , 3 , =x
$x p
$x [ 7 * 1 + ] map p

:Hello . :world! , \s join p

cwd p
ls p

:README.md open

"""

run(cclrc, [], scope)

def main():
    stack = []
    while True:
        sys.stdout.write('>> ')
        line = sys.stdin.readline()
        if not line:
            break
        run(line, stack, scope)

if __name__ == '__main__':
    main()
