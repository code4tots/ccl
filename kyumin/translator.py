"""Translator.

I couldn't find a solid Java JSON parser that converts
parses JSON into standard Java types.

I felt it would be easier to write a translator in Python
that would translate JSON into something easier to process
in Java.
"""
import json
import sys

def Translate(d):
  out = []
  _Translate(d, out)
  return ''.join(out).strip()

def _Translate(d, out):
  if d['type'] == 'block':
    out.append(' block %d %d' % (d['scope'], len(d['stmts'])))
    for statement in d['stmts']:
      _Translate(statement, out)

  elif d['type'] == 'if':
    out.append(' if')
    _Translate(d['cond'], out)
    _Translate(d['a'], out)
    _Translate(d['b'], out)

  elif d['type'] == 'while':
    out.append(' while')
    _Translate(d['cond'], out)
    _Translate(d['body'], out)

  elif d['type'] == 'str':
    out.append(' str %d ' % len(d['value']))
    out.append(' '.join(str(ord(c)) for c in d['value']))

  elif d['type'] in ('float', 'int', 'name'):
    out.append(' %s %s' % (d['type'], d['value']))

  elif d['type'] == 'call':
    out.append(' call')
    _Translate(d['f'], out)
    out.append(' %d' % len(d['args']))
    for arg in d['args']:
      _Translate(arg, out)

  elif d['type'] in ('decl', 'assign'):
    out.append(' %s %s' % (d['type'], d['name']))
    _Translate(d['value'], out)

  elif d['type'] == 'lambda':
    out.append(' lambda %d %s %s' % (
        len(d['names']), ' '.join(d['names']), d['varargs']))
    _Translate(d['body'], out)

  else:
    raise ValueError(d)


if __name__ == '__main__':
  print(Translate(json.loads(sys.stdin.read())))
