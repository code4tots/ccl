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
  import kivy.uix.stacklayout
  import kivy.uix.boxlayout
  import kivy.vector

  def MakeApp():
    d = dict()
    app = kivy.app.App()
    app.build = lambda: d['build']()['rawPython']

    def SetTitle(title):
      app.title = title

    d.update({
        'setTitle': SetTitle,
        'run': app.run,
        'rawPython': app,
    })
    return d

  def BindWidgetMethods(d, widget):

    def AddWidget(child):
      widget.add_widget(child['rawPython'])
    d['addWidget'] = AddWidget

  def MakeWidget(dd=None):
    dd = dd or dict()
    widget = kivy.uix.widget.Widget()
    d = dict()
    BindWidgetMethods(d, widget)
    d.update({
        'rawPython': widget,
    })
    return d

  def MakeLabel(dd):
    if isinstance(dd, str):
      dd = {'text': dd}

    label = kivy.uix.label.Label()
    d = dict()

    def SetText(text):
      label.text = text

    def GetText():
      return label.text

    d.update({
        'getText': GetText,
        'setText': SetText,
        'rawPython': label,
    })
    label.text = dd['text']
    return d

  # TODO: StackLayout doesn't work as expected...
  def MakeStackLayout(dd=None):
    dd = dd or dict()
    stackLayout = kivy.uix.stacklayout.StackLayout()
    d = dict()
    BindWidgetMethods(d, stackLayout)
    d.update({
        'rawPython': stackLayout,
    })
    return d

  def MakeBoxLayout(dd=None):
    dd = dd or dict()
    boxLayout = kivy.uix.boxlayout.BoxLayout()
    d = dict()
    BindWidgetMethods(d, boxLayout)
    d.update({
        'rawPython': boxLayout,
    })
    return d

  return {
      'rawKivyModule': kivy,
      'app': MakeApp,
      'uix': {
          'widget': MakeWidget,
          'label': MakeLabel,
          'stackLayout': MakeStackLayout,
          'boxLayout': MakeBoxLayout,
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

def EvalStr(string, ctx=None):
  return Eval(json.loads(string), ctx or Context(GLOBAL))

def Eval(data, ctx):
  if data['type'] == 'str':
    return str(data['value'])
  elif data['type'] == 'float':
    return float(data['value'])
  elif data['type'] == 'int':
    return int(data['value'])
  elif data['type'] == 'name':
    return ctx[data['value']]
  elif data['type'] == 'call':
    f = Eval(data['f'], ctx)
    args = [Eval(arg, ctx) for arg in data['args']]
    return f(*args)
  elif data['type'] == 'block':
    if data['scope']:
      ctx = Context(ctx)
    last = 0
    for statement in data['statements']:
      last = Eval(statement, ctx)
    return last
  elif data['type'] in ('decl', 'assign'):
    value = Eval(data['value'], ctx)
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
      return Eval(data['body'], ctx)
    return Lambda
  elif data['type'] == 'if':
    return Eval(data['a' if Eval(data['cond'], ctx) else 'b'], ctx)
  elif data['type'] == 'while':
    last = 0
    while Eval(data['cond'], ctx):
      last = Eval(data['body'], ctx)
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
  EvalStr(sys.stdin.read())
