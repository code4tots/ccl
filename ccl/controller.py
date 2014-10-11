import ccl.exception as ex
from ccl.scope import global_scope, new_scope
from ccl.parser import parse

def run(string, file_name = '', scope = None):
    if scope is None:
        scope = new_scope(global_scope)
    
    try:
        return parse(string, file_name)(scope)
    except ex.CclException as e:
        print(e)

def run_file(file_name, scope = None):
    with open(file_name) as f:
        run(f.read(), file_name, scope)

def partially_formed(string):
    inners = '([{'
    outers = ')]}'
    depth = 0
    for token in lex(string):
        if token.type in inners:
            depth += 1
        elif token.type in outers:
            depth -= 1
        
        if depth < 0:
            return False
    
    return depth > 0

def repl():
    while True:
        command = input('>>> ')
        while partially_formed(command):
            command += input('... ')
        result = run(command)
        if result is not None:
            print(result)
