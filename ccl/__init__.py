try:
    input = raw_input
except NameError:
    pass

from ccl.lexer   import lex
from ccl.parser  import Parser
from ccl.context import new_context

def run(string, context = None):
    if context is None:
        context = new_context()
    Parser(string).all()(context)

def repl(context = None):
    if context is None:
        context = new_context()
    
    def count(type_):
        return sum(t.type == type_ for t in lex(command_string))
    
    try:
        while True:
            command_string = input('>>> ').strip()
            if command_string == '':
                continue
            while count('(') != count(')') or count('{') != count('}'):
                command_string += input('... ')
            run(command_string, context)
    except EOFError:
        print('')
