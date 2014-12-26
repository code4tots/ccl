from collections import namedtuple
Token = namedtuple('Token', 'type value text mark')
KEYWORDS = ['for']
SYMBOLS = list(sorted(
    ('+', '-', '*', '/', '=', '(', ')', ';', ','),
    reverse=True))

class Lexer(object):

  def __init__(self, text, mark=0):
    self._text = text
    self._mark = mark

  def __iter__(self):
    return self

  def __next__(self):
    return self.next()

  @property
  def _c(self):
    return self._text[self._mark]

  def next(self):
    if self._mark > len(self._text):
      raise StopIteration()

    while self._mark < len(self._text) and self._c.isspace():
      self._mark += 1

    mark = self._mark

    if self._mark == len(self._text):
      self._mark += 1
      return Token(
          type='EOF',
          value=None,
          text=self._text,
          mark=mark)

    if self._c.isdigit() or self._c == '.':
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
            mark=mark)
      else:
        return Token(
            type='INT',
            value=int(self._text[mark:self._mark]),
            text=self._text,
            mark=mark)

    if self._c.isalpha() or self._c == '_':
      while self._c.isalpha() or self._c == '_':
        self._mark += 1
      string = self._text[mark:self._mark]
      return Token(
          type=string if string in KEYWORDS else 'NAME',
          value=string,
          text=self._text,
          mark=mark)

    if self._c in ('"',"'"):
      q = self._c
      self._mark += 1
      while self._c != q:
        self._mark += 2 if self._c == '\\' else 1
      self._mark += 1
      return Token(
          type='STRING',
          value=eval(self._text[mark:self._mark]),
          text=self._text,
          mark=mark)

    for symbol in SYMBOLS:
      if self._text.startswith(symbol, self._mark):
        self._mark += len(symbol)
        return Token(
            type=symbol,
            value=symbol,
            text=self._text,
            mark=mark)

    raise SyntaxError(self._mark)
