"""LL(1) grammar. Nuff said.
"""

from ccl.lexer import lex
from ccl.ast   import Int, Float, String, Name, Command, Block

class Parser(object):
    atom_start_token_types = frozenset(
        ('(','{','INT','FLOAT','STRING','NAME'))
    
    def __init__(self, string):
        self.generator = lex(string)
        self.lookahead = next(self.generator)
    
    def next_token(self):
        token = self.lookahead
        self.lookahead = next(self.generator)
        return token
    
    def expect(self, type_):
        if self.lookahead.type != type_:
            raise SyntaxError('expected %r but got %r' %
                (type_, self.type))
        return self.next_token()
    
    def skip_newlines(self):
        while self.lookahead.type in ';\n':
            self.next_token()
    
    def atom(self):
        if self.lookahead.type == 'INT':
            return Int(self.next_token().value)
        elif self.lookahead.type == 'FLOAT':
            return Float(self.next_token().value)
        elif self.lookahead.type == 'STRING':
            return String(self.next_token().value)
        elif self.lookahead.type == 'NAME':
            return Name(self.next_token().value)
        elif self.lookahead.type == '{':
            self.next_token()
            block = Block(self.commands())
            self.expect('}')
            return block
        elif self.lookahead.type == '(':
            self.next_token()
            command = self.command()
            self.expect(')')
            return command
        raise SyntaxError('expected atom but found %r' %
            (self.lookahead.type,))
    
    def command(self):
        f = self.atom()
        args = []
        while self.lookahead.type in self.atom_start_token_types:
            args.append(self.atom())
        return Command(f,args)
    
    def commands(self):
        self.skip_newlines()
        commands = []
        while self.lookahead.type in self.atom_start_token_types:
            commands.append(self.command())
            self.skip_newlines()
        return commands
    
    def all(self):
        return Block(self.commands())
