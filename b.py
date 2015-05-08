import re

TOKEN_REGEXES = tuple(re.compile(pattern, re.MULTILINE|re.DOTALL) for pattern in (
  r'\(', r'\)',
  r'[0-9]+\.[0-9]*',
  r'\.[0-9]+',
  r'[0-9]+',
  r'\"(\\\"|[^"])*\"',
  r'\"\"\"(\\\"|[^"])*\"\"\"',
  r'r\".*?\"',
  r'r\"\"\".*?\"\"\"',
  r"\'(\\\'|[^'])*\'",
  r"\'\'\'(\\\'|[^'])*\'\'\'",
  r"r\'.*?\'",
  r"r\'\'\'.*?\'\'\'",
  r'[a-zA-Z0-9_]+',
  r'\s+'))

def lex(s):
  i = 0
  while i < len(s):
    for r in TOKEN_REGEXES:
      m = r.match(s, i)
      if m:
        t = m.group()
        if not t.strip():
          pass
        elif t in ('(', ')'):
          yield {'type': t, 'i': i, 's': s}
        else:
          try:
            yield {'type': 'int', 'value': int(t), 'i': i, 's': s}
          except ValueError:
            try:
              yield {'type': 'float', 'value': float(t), 'i': i, 's': s}
            except ValueError:
              if t.startswith(('r"', "r'", '"', "'")):
                yield {'type': 'str', 'value': eval(t), 'i': i, 's': s}
              else:
                yield {'type': 'id', 'value': t, 'i': i, 's': s}
        i = m.end()
        break
    else:
      raise SyntaxError((s, i))

def parse(s):
  stack = [[]]
  for token in lex(s):
    if token['type'] == '(':
      stack.append([token])
    elif token['type'] == ')':
      args = stack.pop()
      t = args[0]
      items = args[1:]
      t['type'] = 'list'
      t['value'] = items
      stack[-1].append(t)
    else:
      stack[-1].append(token)
  assert len(stack) == 1, stack
  return stack[0]

print(list(parse("""
hello (world)
""")))
