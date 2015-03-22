# Uses python3 version of antlr

import collections
import os
import sys
import urllib.request

import antlr4

import BubLexer
import BubListener
import BubParser


def NamedTuple(attrs):
  return collections.namedtuple('namedtuple', attrs)


class CclObject(object):
  pass


class Nil(CclObject):
  _instance = None

  def __new__(cls):
    if cls._instance is None:
      cls._instance = super(Nil, cls).__new__(cls)

    return cls._instance

  def __bool__(self):
    return False

  def __repr__(self):
    return 'nil'


class Bool(int, CclObject):

  def __str__(self):
    return repr(self)

  def __repr__(self):
    return 'true' if self else 'false'


class Num(float, CclObject):

  def __str__(self):
    return repr(self)

  def __repr__(self):
    return str((int if self == int(self) else float)(self))


class Str(str, CclObject):
  pass


class List(list, CclObject):

  def __hash__(self):
    return hash(tuple(self))


class Dict(dict, CclObject):

  def __hash__(self):
    return hash(frozenset(self.items()))


class Lambda(NamedTuple('args body ctx'), CclObject):

  def __call__(self, *args):
    ctx = Context(self.ctx)
    ctx.Update(dict(zip(self.args, args)))
    return self.body.Eval(ctx)


class Builtin(CclObject):

  def __init__(self, f, name=None):
    self.f = f
    self.name = name or f.__name__

  def __call__(self, *args, **kwargs):
    result = self.f(*args, **kwargs)
    if not isinstance(result, CclObject):
      raise ValueError('%s is not a CclObject' % (result,))
    return result

  def __repr__(self):
    return "<builtin '%s'>" % self.name


class Context(object):

  def __init__(self, parent=None):
    self.table = dict()
    self.parent = parent

  def __getitem__(self, name):
    if self.parent is None and name not in self.table:
      raise KeyError(name)
    return self.table[name] if name in self.table else self.parent[name]

  def __setitem__(self, name, value):
    assert isinstance(name, str)
    assert isinstance(value, CclObject)
    (self.table if name in self.table else self.parent)[name] = value

  def Update(self, d):
    assert all(isinstance(key, str) for key in d.keys())
    assert all(isinstance(value, CclObject) for value in d.values())
    self.table.update(d)

  def Declare(self, name):
    assert isinstance(name, str)
    self.table[name] = Nil()


class Display(object):
  pass


class NumDisplay(str, Display):

  def Eval(self, ctx):
    return Num(self)


class StrDisplay(str, Display):

  def Eval(self, ctx):
    return Str(eval(self))


class IdDisplay(str, Display):

  def Eval(self, ctx):
    return ctx[str(self)]


class BasicCmdDisplay(NamedTuple('f args kwargs'), Display):

  def Eval(self, ctx):
    f = self.f.Eval(ctx)
    args = [d.Eval(ctx) for d in self.args]
    kwargs = {kw:v.Eval(ctx) for kw, v in self.kwargs.items()}

    return f(*args, **kwargs) if isinstance(f, (Builtin, Lambda)) else f


class LambdaDisplay(NamedTuple('args body'), Display):

  def Eval(self, ctx):
    self.args


class BlockDisplay(tuple, Display):

  def Eval(self, ctx):
    last = None
    for d in self:
      last = d.Eval(ctx)
    return last


class RedirectDisplay(NamedTuple('src dest'), Display):

  def Eval(self, ctx):
    data = self.src.Eval(ctx)
    dest = self.dest.Eval(ctx)
    with open(dest, 'w') as f:
      f.write(data)
    return data


class AssignDisplay(NamedTuple('name value'), Display):

  def Eval(self, ctx):
    ctx[self.name] = value = self.value.Eval(ctx)
    return value


class DeclareDisplay(NamedTuple('name value'), Display):

  def Eval(self, ctx):
    ctx.Declare(self.name)
    ctx[self.name] = value = self.value.Eval(ctx)
    return value


class Listener(BubListener.BubListener):

  @classmethod
  def SelectBinOpDisplayClass(cls, op):
    if op == '*':
      return MulDisplay
    elif op == '+':
      return AddDisplay
    raise ValueError('%s is not a binary operator' % (op,))

  def __init__(self):
    self.stack = self.result = None

  def PushStack(self):
    self.stack.append([])

  def PopStack(self):
    return self.stack.pop()

  def Push(self, display):
    self.stack[-1].append(display)

  def Pop(self):
    return self.stack[-1].pop()

  def enterStart(self, ctx):
    self.stack = [[]]
    self.result = None

  def exitStart(self, ctx):
    assert len(self.stack) == 1
    assert len(self.stack[0]) == 1
    self.result = self.stack[0][0]
    self.stack = None

  def enterStmts(self, ctx):
    self.PushStack()

  def exitStmts(self, ctx):
    self.Push(BlockDisplay(self.PopStack()))

  def exitNumExpr(self, ctx):
    self.Push(NumDisplay(ctx.atom.text))

  def exitStrExpr(self, ctx):
    self.Push(StrDisplay(ctx.atom.text))

  def exitIdExpr(self, ctx):
    self.Push(IdDisplay(ctx.atom.text))

  def enterArgs(self, ctx):
    self.PushStack()

  def exitArgs(self, ctx):
    args = list()
    kwargs = dict()
    for arg in self.PopStack():
      if isinstance(arg, Display):
        args.append(arg)
      else:
        kw, value = arg
        kwargs[kw] = value
    self.Push((args, kwargs))

  def exitBasicCmd(self, ctx):
    args, kwargs = self.Pop()
    f = self.Pop()
    self.Push(BasicCmdDisplay(f, args, kwargs))

  def exitRedirectCmd(self, ctx):
    dest = self.Pop()
    src = self.Pop()
    self.Push(RedirectDisplay(src, dest))

  def exitDeclareCmd(self, ctx):
    self.Push(DeclareDisplay(ctx.name.text, self.Pop()))

  def exitAssignCmd(self, ctx):
    self.Push(AssignDisplay(ctx.name.text, self.Pop()))


def builtin_p(*args):
  print(*args)
  return args[-1] if args else Nil()


def builtin_j(x):
  return x


def builtin_expand(path):
  return Str(os.path.expandvars(os.path.expanduser(path)))


def builtin_ls(path='.'):
  return List(os.listdir(builtin_expand(path)))


def builtin_cwd():
  return Str(os.getcwd())


def builtin_cd(path='~'):
  os.chdir(builtin_expand(path))
  return Nil()


def builtin_get(url):
  with urllib.request.urlopen(url) as f:
    return Str(f.read().decode('utf-8'))


def run(source, ctx, fromfile=False):
  if fromfile:
    inp = antlr4.FileStream(source)
  else:
    inp = antlr4.InputStream.InputStream(source)

  lexer = BubLexer.BubLexer(inp)
  stream = antlr4.CommonTokenStream(lexer)
  parser = BubParser.BubParser(stream)
  tree = parser.start()
  walker = antlr4.ParseTreeWalker()
  listener = Listener()
  walker.walk(listener, tree)

  return listener.result.Eval(ctx)


def main():
  ctx = Context()
  ctx.Update({
      'nil': Nil(),
      'true': Bool(True),
      'false': Bool(False),

      '~': Str('~'),
      '.': Str('.'),
      '..': Str('..'),

      'p': Builtin(builtin_p, 'p'),
      'expand': Builtin(builtin_expand, 'expand'),
      'j': Builtin(builtin_j, 'j'),
      'ls': Builtin(builtin_ls, 'ls'),
      'cwd': Builtin(builtin_cwd, 'cwd'),
      'cd': Builtin(builtin_cd, 'cd'),

      'get': Builtin(builtin_get, 'get'),
  })

  if len(sys.argv) > 1:
    inp = run(sys.argv[1], ctx, fromfile=True)
  else:
    try:
      while True:
        result = run(input('>> '), ctx, fromfile=False)
        if result is not Nil():
          print(result)
    except EOFError:
      print()


if __name__ == '__main__':
  main()
