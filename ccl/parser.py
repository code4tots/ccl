"""parser.py
ccl has LL(1) grammar
"""
def parse(string, file_name = ''):
    from ccl.exception import UnexpectedToken, ExpectedAtom
    from ccl.lexer import lex
    
    generator = lex(string, file_name)
    lookahead = [next(generator)]
    
    def next_token():
        token = lookahead[0]
        lookahead[0] = next(generator)
        return token
    
    def expect(t):
        if lookahead[0].type != t:
            raise UnexpectedToken(lookahead[0], t)
        return next_token()
    
    def consume(t):
        if lookahead[0].type == t:
            return next_token()
    
    def multiple(rule, skip_newlines):
        elements = []
        
        while True:
            if skip_newlines:
                skip_lines()
            
            if lookahead[0].type not in rule.start_symbols:
                break
            
            elements.append(rule())
        
        return elements
    
    def skip_lines():
        while lookahead[0].type in (';','\n'):
            next_token()
    
    def all_():
        from ccl.lexer import Token, Location
        from ccl.ast import Block
        return Block(
            Token(None, None, Location(string, 0, 1, file_name)),
            multiple(command, skip_newlines=True))
    
    def atom():
        if lookahead[0].type.isalpha():
            from ccl.ast import (
                IntDisplay,
                FloatDisplay,
                StringDisplay,
                NameDisplay)
            t = lookahead[0].type
            r = locals()[t+'Display'](next_token())
        elif lookahead[0].type == '[':
            from ccl.ast import ListDisplay
            r = ListDisplay(
                next_token(),
                multiple(atom, skip_newlines=True))
            expect(']')
        elif consume('('):
            r = command()
            expect(')')
        elif lookahead[0].type == '{':
            from ccl.ast import Block
            r = Block(
                next_token(),
                multiple(command, skip_newlines=True))
            expect('}')
        else:
            raise ExpectedAtom(lookahead[0])
        
        while consume('.'):
            from ccl.ast import AttributeDisplay
            r = AttributeDisplay(r, expect('Name').value)
        
        return r
    
    def command():
        from ccl.ast import Command
        f = atom()
        args = multiple(atom, skip_newlines=False)
        if consume('$'):
            args.append(command())
        return Command(f,args)
    
    atom.start_symbols = (
        'String', 'Float', 'Int', 'Name',
        '(', '{', '[')
    
    command.start_symbols = atom.start_symbols
    
    return all_()
