class Ast(collections.namedtuple('Ast', 'string position value')):
  def __eq__(self, other):
    return type(self) == type(other) and super(Ast, self).__eq__(other)

def get_line(string, i):
  begin = string.rfind('\n', 0, i) + 1
  end = string.find('\n', i)
  end = len(string) if end == -1 else end
  return string[begin:end]

def get_line_number(string, i):
  return string.count('\n', i) + 1

def get_column_number(string, i):
  return i - string.rfind('\n', 0, i)

def make_location_message(string, i):
  return 'on line %s\n%s\n%s*' % (
      get_line_number(string, i),
      get_line(string, i),
      ' ' * (get_column_number(string, i) - 1))

def parse(string, StringLiteral, Name, Number, List):
  s = string
  i = 0
  e = [[]]
  p = []

  while i < len(s) and s[i].isspace():
    i += 1

  while i < len(s):
    j = i
    c = s[i+1:i+2]
    d = s[i+2:i+3]

    if s[i] == '(':
      e.append([])
      p.append(i)
      i += 1

    elif s[i] == ')':
      if not p:
        raise SyntaxError('Unexpected close parenthesis ' + make_location_message(s, p[-1]))
      e[-2].append(List(s, p.pop(), tuple(e.pop())))
      i += 1

    elif s[i] in '"\'':
      i += 1
      while i < len(s) and s[i] != s[j]:
        i += 2 if s[i] == '\\' else 1
      if i >= len(s):
        raise SyntaxError('Unterminated string literal ' + make_location_message(s, j))
      i += 1
      e[-1].append(StringLiteral(s, j, s[j:i]))

    elif s[i].isdigit() or s[i] in '-.' and c.isdigit() or s[i:i+2] == '-.' and d.isdigit():
      if s[i] in '-':
        i += 1

      while i < len(s) and s[i].isdigit():
        i += 1

      if i < len(s) and s[i] == '.':
        i += 1
        while i < len(s) and s[i].isdigit():
          i += 1

      e[-1].append(Number(s, j, s[j:i]))

    elif s[i].isalpha() or s[i] in '_':
      while i < len(s) and (s[i].isalnum() or s[i] in '_'):
        i += 1

      e[-1].append(Name(s, j, s[j:i]))

    else:
      raise SyntaxError('Invalid token ' + make_location_message(s, j))

    while i < len(s) and s[i].isspace():
      i += 1

  if p:
    raise SyntaxError('Unterminated parenthesis ' + make_location_message(s, j))

  return e[0]

s = """
Hello World!
"""

assert get_line(s, 1) == 'Hello World!'
assert get_line_number(s, 1) == 2
assert get_column_number(s, 1) == 1
assert make_location_message(s, 1) == 'on line 2\nHello World!\n*'

s = """
(a (hello world "way to go there") 5.5)
"""

def only_value(string, position, value):
  return value

assert parse(s, StringLiteral=only_value, Name=only_value, Number=only_value, List=only_value) == [
    ('a', ('hello', 'world', '"way to go there"'), '5.5')]
