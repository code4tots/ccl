import operator
from collections import namedtuple

Token = namedtuple('Token', 'type value text mark')
KEYWORDS = ['for']
SYMBOLS = list(sorted(
    ('+', '-', '*', '/', '=', '(', ')'),
    reverse=True))


class Lexer(object):

  def __init__(self, text, mark=0):
    self._text = text
    self._mark = mark

  def __iter__(self):
    return self

  @property
  def _c(self):
    return self._text[self._mark]

  def next(self):
    if self._mark > len(self._text):
      raise StopIteration()

    while self._mark < len(self._text) and self._c.isspace():
      self._mark += 1

    if self._mark == len(self._text):
      self._mark += 1
      return Token(
          type='EOF',
          value=None,
          text=self._text,
          mark=self._mark-1)

    if self._c.isdigit() or self._c == '.':
      mark = self._mark
      while self._c.isdigit():
        self._mark += 1
      if self._c == '.':
        self._mark += 1
        while self._c.isdigit():
          self._mark += 1
        return Token(
            type='FLOAT',
            value=float(self._text[mark:self._mark]),
            text=self._text,
            mark=self._mark)
      else:
        return Token(
            type='INT',
            value=int(self._text[mark:self._mark]),
            text=self._text,
            mark=self._mark)

    if self._c.isalpha() or self._c == '_':
      mark = self._mark
      while self._c.isalpha() or self._c == '_':
        self._mark += 1
      string = self._text[mark:self._mark]
      return Token(
          type=string if string in KEYWORDS else 'NAME',
          value=string,
          text=self._text,
          mark=self._mark)

    if self._c in ('"',"'"):
      mark = self._mark
      q = self._c
      self._mark += 1
      while self._c != q:
        self._mark += 2 if self._c == '\\' else 1
      self._mark += 1
      return Token(
          type='STRING',
          value=eval(self._text[mark:self._mark]),
          text=self._text,
          mark=self._mark)

    for symbol in SYMBOLS:
      if self._text.startswith(symbol, self._mark):
        self._mark += len(symbol)
        return Token(
            type=symbol,
            value=symbol,
            text=self._text,
            mark=self._mark)

    raise SyntaxError(self._mark)


class Parser(object):

  def __init__(self, lexer):
    self._lexer = lexer
    self._peek = lexer.next()

  def next(self):
    pass

  def consume(self, construct):
    if isinstance(construct, str):
      if self._peek.type == construct:
        token = self._peek
        self._peek = self._lexer.next()
        return token
    else:
      return construct()

  def expect(self, construct):
    result = self.consume(construct)
    if result is None:
      raise SyntaxError((construct, self._peek))
    return result

  def token_atom(self, type_):
    token = self.consume(type_)
    if token is not None:
      def thunk(context):
        return token.value
      return thunk

  def parenthetical_expression(self):
    if self.consume('('):
      expression = self.expression()
      self.expect(')')
      return expression

  def atom(self):
    return (
        self.token_atom('INT') or
        self.token_atom('FLOAT') or
        self.token_atom('STRING') or
        self.token_atom('NAME') or
        self.parenthetical_expression())

  def sign_expression(self):
    if self.consume('+'):
      return self.expect(self.sign_expression)
    elif self.consume('-'):
      expression = self.expect(self.sign_expression)
      def thunk(context):
        return -expression(context)
      return thunk
    else:
      return self.atom()

  def multiplicative_expression(self):
    lhs = self.sign_expression()
    while True:
      op = (
          operator.mul     if self.consume('*') else
          operator.truediv if self.consume('/') else
          operator.mod     if self.consume('%') else
          None)
      if op is None: break
      rhs = self.expect(self.sign_expression)
      def scope(op, lhs, rhs):
        def thunk(context):
          return op(lhs(context), rhs(context))
        return thunk
      lhs = scope(op, lhs, rhs)
    return lhs

  def additive_expression(self):
    lhs = self.multiplicative_expression()
    while True:
      op = (
          operator.add     if self.consume('+') else
          operator.sub     if self.consume('-') else
          None)
      if op is None: break
      rhs = self.expect(self.multiplicative_expression)
      def scope(op, lhs, rhs):
        def thunk(context):
          return op(lhs(context), rhs(context))
        return thunk
      lhs = scope(op, lhs, rhs)
    return lhs

  def expression(self):
    return self.additive_expression()

text = """

"hi " + "there"

"""

thunk = Parser(Lexer(text)).expression()

print(thunk(dict()))
