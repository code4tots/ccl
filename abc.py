from __future__ import print_function
import operator
from collections import namedtuple

Token = namedtuple('Token', 'type value text mark')
KEYWORDS = ['for']
SYMBOLS = list(sorted(
    ('+', '-', '*', '/', '=', '(', ')', ';', ','),
    reverse=True))


class Thunk(object):
  pass


class AssignableThunk(Thunk):
  pass


class LiteralThunk(Thunk):

  def __init__(self, value):
    self.value = value

  def __call__(self, context):
    return self.value


class NameThunk(AssignableThunk):

  def __init__(self, name):
    self.name = name

  def __call__(self, context):
    return context[self.name]

  def assign(self, context, value):
    context[self.name] = value
    return value


class FunctionCallThunk(Thunk):

  def __init__(self, function, arguments):
    self.function = function
    self.arguments = arguments


  def __call__(self, context):
    return self.function(context)(*[arg(context) for arg in self.arguments])


class FunctionCallSyntacticSugarThunk(FunctionCallThunk):

  def __init__(self, *arguments):
    self.arguments = arguments


class NegThunk(FunctionCallSyntacticSugarThunk):
  function = NameThunk('__neg__')


class PosThunk(FunctionCallSyntacticSugarThunk):
  function = NameThunk('__pos__')


class AddThunk(FunctionCallSyntacticSugarThunk):
  function = NameThunk('__add__')


class SubThunk(FunctionCallSyntacticSugarThunk):
  function = NameThunk('__sub__')


class MulThunk(FunctionCallSyntacticSugarThunk):
  function = NameThunk('__mul__')


class TrueDiv(FunctionCallSyntacticSugarThunk):
  function = NameThunk('__truediv__')


class ModThunk(FunctionCallSyntacticSugarThunk):
  function = NameThunk('__mod__')


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
    self._peek_stack = [lexer.next()]

  @property
  def _peek(self):
    return self._peek_stack[-1]

  def next(self):
    self._peek_stack.pop()
    if not self._peek_stack:
      self._peek_stack = [self._lexer.next()]

  def put_back(self, token):
    self._peek_stack.append(token)

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
      return LiteralThunk(token.value)

  def name_expression(self):
    token = self.consume('NAME')
    if token is not None:
      return NameThunk(token.value)

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
        self.parenthetical_expression())

  def function_call_expression(self):
    lhs = self.atom_expression()
    while self.consume('('):
      args = []
      if not self.consume(')'):
        args.append(self.expect(self.expression))
        while not self.consume(')'):
          self.expect(',')
          args.append(self.expect(self.expression))
      lhs = FunctionCallThunk(lhs, args)
    return lhs

  def sign_expression(self):
    if self.consume('+'):
      return PosThunk(self.expect(self.sign_expression))
    elif self.consume('-'):
      return NegThunk(self.expect(self.sign_expression))
    else:
      return self.function_call_expression()

  def multiplicative_expression(self):
    lhs = self.sign_expression()
    while True:
      op = (
          MulThunk   if self.consume('*') else
          TrueDiv    if self.consume('/') else
          ModThunk   if self.consume('%') else
          None)
      if op is None: break
      lhs = op(lhs, self.expect(self.sign_expression))
    return lhs

  def additive_expression(self):
    lhs = self.multiplicative_expression()
    while True:
      op = (
          AddThunk     if self.consume('+') else
          SubThunk     if self.consume('-') else
          None)
      if op is None: break
      lhs = op(lhs, self.expect(self.multiplicative_expression))
    return lhs

  def assignment_expression(self):
    name = self.consume('NAME')
    if name:
      equal = self.consume('=')
      if equal:
        lhs = name.value
        rhs = self.assignment_expression()
        def thunk(context):
          context[lhs] = value = rhs(context)
          return value
        return thunk
      else:
        self.put_back(name)
    return self.additive_expression()

  def semicolon_expression(self):
    lhs = self.assignment_expression()
    while True:
      op = (
          (lambda a, b: b)   if self.consume(';') else
          None)
      if op is None: break
      rhs = self.expect(self.assignment_expression)
      def scope(op, lhs, rhs):
        def thunk(context):
          return op(lhs(context), rhs(context))
        return thunk
      lhs = scope(op, lhs, rhs)
    return lhs

  def expression(self):
    return self.semicolon_expression()

text = r"""

y = x = "hi " + "there" ; z = "I see." ; print(y + '\n' + y, 'fi') ;
print(+5 + -3 - 7) ;
print(5 / 2)

"""

thunk = Parser(Lexer(text)).expression()

thunk({
    '__mul__': operator.mul,
    '__truediv__': operator.truediv,
    '__mod__': operator.mod,
    '__add__': operator.add,
    '__sub__': operator.sub,
    '__pos__': operator.pos,
    '__neg__': operator.neg,
    'print': print
})
