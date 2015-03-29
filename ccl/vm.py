import json
import sys

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
  if data['type'] in ('str', 'float', 'int'):
    return data['value']
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
  raise ValueError(data)

GLOBAL = Context(None, {
  'print': print,
})

if __name__ == '__main__':
  EvalStr(Context(GLOBAL), sys.stdin.read())
