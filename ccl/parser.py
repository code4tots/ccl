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
