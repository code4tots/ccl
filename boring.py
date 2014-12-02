"""S-expression grammar."""
from collections import namedtuple

SYMBOLS = ('(', ')')
Token = namedtuple('Token', 'type value position')
List = namedtuple('List', 'position values')

def lex(string):
  start = [0]
  end = [0]
  def char():          return string[end[0]:end[0]+1]
  def last():          return string[end[0]-1:end[0]]
  def cut():           return string[start[0]:end[0]]
  def token(type):     return Token(type, cut(), start[0])
  def skip(predicate):
    while predicate(): end[0] += 1

  while True:
    skip(lambda: char().isspace())
    start[0] = end[0]
    if not char(): break
    if char().isdigit():
      skip(lambda: char().isdigit())
      if char() == '.':
        end[0] += 1
        skip(lambda: char().isdigit())
        yield token('FLOAT')
      else:
        yield token('INT')
    elif char().isalpha() or char() == '_':
      skip(lambda: char().isalnum() or char() == '_')
      yield token('ID')
    elif char() in ('"',"'"):
      quote = char()
      end[0] += 1
      skip(lambda: char() != quote or last() == '\\')
      end[0] += 1
      yield token('STRING')
    elif any(string.startswith(symbol, start[0]) for symbol in SYMBOLS):
      sym = next(s for s in SYMBOLS if string.startswith(s, start[0]))
      end[0] += len(sym)
      yield token(sym)
    else:
      skip(lambda: not char().isspace())
      raise SyntaxError(cut())
  yield token('EOF')

def parse(token_stream):
  stack = [[]]
  for token in token_stream:
    if token.type == '(':
      stack.append([token.position])
    elif token.type == ')':
      position, *values = stack.pop()
      stack[-1].append(List(position, values))
    else:
      stack[-1].append(token)
  assert len(stack) == 1, 'unclosed parenthesis'
  return stack[0]



print(parse(lex("""
(list (1 2 3 4))

(a (id 'homepage'))

""")))
