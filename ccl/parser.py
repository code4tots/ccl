"""LL(1) grammar. Nuff said.
"""

from ccl.lexer import lex
from ccl.ast   import Int, Float, String, Name, Command, Block, Attribute

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
    
    def consume(self, type_):
        if self.lookahead.type == type_:
            return self.next_token()
    
    def skip_newlines(self):
        while self.lookahead.type in ';\n':
            self.next_token()
    
    def atom(self):
        if self.lookahead.type == 'INT':
            return_value = Int(self.next_token().value)
        elif self.lookahead.type == 'FLOAT':
            return_value = Float(self.next_token().value)
        elif self.lookahead.type == 'STRING':
            return_value = String(self.next_token().value)
        elif self.lookahead.type == 'NAME':
            return_value = Name(self.next_token().value)
        elif self.consume('{'):
            block = Block(self.commands())
            self.expect('}')
            return_value = block
        elif self.consume('('):
            command = self.command()
            self.expect(')')
            return_value = command
        else:
            raise SyntaxError('expected atom but found %r' %
                (self.lookahead.type,))
        
        while self.consume('.'):
            return_value = Attribute(
                return_value,
                self.next_token().value)
        
        return return_value
            
    
    def atoms(self, skip_newlines):
        atoms = []
        
        if skip_newlines:
            self.skip_newlines()
        
        while self.lookahead.type in self.atom_start_token_types:
            atoms.append(self.atom())
            
            if skip_newlines:
                self.skip_newlines()
        
        return atoms
    
    def command(self):
        f = self.atom()
        args = self.atoms(skip_newlines = False)
        return Command(f,args)
    
    def commands(self):
        commands = []
        self.skip_newlines()
        while self.lookahead.type in self.atom_start_token_types:
            commands.append(self.command())
            self.skip_newlines()
        return commands
    
    def all(self):
        return Block(self.commands())
