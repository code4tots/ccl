from . import thunk

class Parser(object):

  def __init__(self, lexer):
    self._lexer = lexer
    self._peek = lexer.next()

  def next(self):
    self._peek = self._lexer.next()

  def consume(self, construct):
    if isinstance(construct, str):
      if self._peek.type == construct:
        token = self._peek
        self.next()
        return token
    else:
      return construct()

  def expect(self, construct):
    result = self.consume(construct)
    if result is None:
      raise SyntaxError((construct, self._peek))
    return result

  def token_literal_expression(self, type_):
    token = self.consume(type_)
    if token is not None:
      return thunk.Literal(token.value)

  def name_expression(self):
    token = self.consume('NAME')
    if token is not None:
      return thunk.Name(token.value)

  def parenthetical_expression(self):
    if self.consume('('):
      expression = self.expression()
      self.expect(')')
      return expression

  def atom_expression(self):
    return (
        self.token_literal_expression('INT') or
        self.token_literal_expression('FLOAT') or
        self.token_literal_expression('STRING') or
        self.name_expression() or
        self.parenthetical_expression() or
        None)

  def expression(self):
    return self.atom_expression()
