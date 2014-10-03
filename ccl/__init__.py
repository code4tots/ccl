try:
    input = raw_input
except NameError:
    pass

from ccl.lexer   import lex
from ccl.parser  import Parser
from ccl.context import new_context
from os import getcwd

def run(string, context = None):
    if context is None:
        context = new_context()
    return Parser(string).all()(context)

def repl(context = None):
    if context is None:
        context = new_context()
    
    def count(type_):
        return sum(t.type == type_ for t in lex(command_string))
    
    while True:
        try:
            command_string = input(getcwd()+'>> ').strip()
            if command_string == '':
                continue
            while count('(') != count(')') or count('{') != count('}'):
                command_string += '\n' + input('... ')
            result = run(command_string, context)
            if result is not None:
                print(result)
        except EOFError:
            print('')
            break
        except Exception:
            import traceback
            print(traceback.format_exc())
