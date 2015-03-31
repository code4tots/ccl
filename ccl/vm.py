from . import compiler

import json
import operator
import sys

def ImportKivy():
  import kivy
  import kivy.app
  import kivy.clock
  import kivy.properties
  import kivy.uix.label
  import kivy.uix.widget
  import kivy.vector

  def MakeApp():
    class KivyApp(kivy.app.App):
      def build(self):
        return app['build']()
    raw_app = KivyApp()
    app = dict()
    app.update({
        'run': raw_app.run,
    })
    return app

  return {
      'rawKivyModule': kivy,
      'app': MakeApp,
      'uix': {
          'label': lambda text: kivy.uix.label.Label(text=text),
      }
  }

class Context(object):

  def __init__(self, parent=None, table=None):
    self.parent = parent
    self.table = table or dict()

  def __getitem__(self, name):
    if name in self.table:
      return self.table[name]
    elif self.parent is not None:
      return self.parent[name]
    else:
      raise KeyError(name)

  def __setitem__(self, name, value):
    if name in self.table:
      self.table[name] = value
    elif self.parent is not None:
      self.parent[name] = value
    else:
      raise KeyError(name)

  def Declare(self, name, value):
    self.table[name] = value

def EvalStr(ctx, string):
  return Eval(ctx, json.loads(string))

def Eval(ctx, data):
  if data['type'] == 'str':
    return str(data['value'])
  elif data['type'] == 'float':
    return float(data['value'])
  elif data['type'] == 'int':
    return int(data['value'])
  elif data['type'] == 'name':
    return ctx[data['value']]
  elif data['type'] == 'call':
    f = Eval(ctx, data['f'])
    args = [Eval(ctx, arg) for arg in data['args']]
    return f(*args)
  elif data['type'] == 'block':
    if data['scope']:
      ctx = Context(ctx)
    last = 0
    for statement in data['statements']:
      last = Eval(ctx, statement)
    return last
  elif data['type'] in ('decl', 'assign'):
    value = Eval(ctx, data['value'])
    if data['type'] == 'decl':
      ctx.Declare(data['name'], value)
    elif data['type'] == 'assign':
      ctx[data['name']] = value
    return value
  elif data['type'] == 'lambda':
    ctx = Context(ctx)
    def Lambda(*args):
      for name, arg in zip(data['names'], args[:len(data['names'])]):
        ctx.Declare(name, arg)
      if data['varargs']:
        ctx.Declare(data['varargs'], args[len(data['names']):])
      return Eval(ctx, data['body'])
    return Lambda
  elif data['type'] == 'if':
    return Eval(ctx, data['a' if Eval(ctx, data['cond']) else 'b'])
  elif data['type'] == 'while':
    last = 0
    while Eval(ctx, data['cond']):
      last = Eval(ctx, data['body'])
    return last
  raise ValueError(data)

def _SetItem(x, i, v):
  x[i] = v
  return v

def Print(*args):
  # Python2 and Python3 have 'print' that is different enough to be
  # annoying.
  sys.stdout.write(' '.join(str(arg) + ' ' for arg in args) + '\n')

GLOBAL = Context(None, {k:v for d in (
  {
    'Print': Print,
    'ImportKivy': ImportKivy,
    '__list__': lambda *args: list(args),
    '__dict__': lambda *args: dict(zip(args[::2], args[1::2])),
  },
  {v: getattr(operator, v) for v in compiler.BINOP_TABLE.values()},
  {v: getattr(operator, v) for v in compiler.SPECIALOPS},
) for k, v in d.items()})

if __name__ == '__main__':
  EvalStr(Context(GLOBAL), sys.stdin.read())
