# Uses python3 version of antlr

import collections
import sys

import antlr4

import CclLexer
import CclListener
import CclParser


def NamedTuple(attrs):
  return collections.namedtuple("namedtuple", attrs)


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
    return "nil"


class Bool(int, CclObject):

  def __str__(self):
    return repr(self)

  def __repr__(self):
    return "true" if self else "false"


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


class Lambda(NamedTuple("args body ctx"), CclObject):

  def __call__(self, *args):
    ctx = Context(self.ctx)
    ctx.Update(dict(zip(self.args, args)))
    return self.body.Eval(ctx)


class Builtin(CclObject):

  def __init__(self, f, name=None):
    self.f = f
    self.name = name or f.__name__

  def __call__(self, *args):
    return self.f(*args)

  def __repr__(self):
    return "<builtin '%s'>" % self.name


class Context(object):

  def __init__(self, parent=None):
    self.table = dict()
    self.parent = parent

  def __getitem__(self, name):
    return self.table[name] if name in self.table else self.parent[name]

  def __setitem__(self, name, value):
    assert isinstance(name, str)
    assert isinstance(value, CclObject)
    (self.table if name in self.table else self.parent)[name] = value

  def Update(self, d):
    assert all(isinstance(key, str) for key in d.keys())
    assert all(isinstance(value, CclObject) for value in d.values())
    self.table.update(d)


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


class ListDisplay(tuple, Display):

  def Eval(self, ctx):
    return List(d.Eval(ctx) for d in self)


class CallDisplay(NamedTuple("f args"), Display):

  def Eval(self, ctx):
    f = self[0].Eval(ctx)
    args = [d.Eval(ctx) for d in self[1]]
    return f(*args)


class MulDisplay(NamedTuple("lhs rhs"), Display):

  def Eval(self, ctx):
    lhs, rhs = (d.Eval(ctx) for d in self)
    return lhs * rhs


class AddDisplay(NamedTuple("lhs rhs"), Display):

  def Eval(self, ctx):
    lhs, rhs = (d.Eval(ctx) for d in self)
    return lhs + rhs


class BlockDisplay(tuple, Display):

  def Eval(self, ctx):
    last = None
    for d in self:
      last = d.Eval(ctx)
    return last


class Listener(CclListener.CclListener):

  @classmethod
  def SelectBinOpDisplayClass(cls, op):
    if op == "*":
      return MulDisplay
    elif op == "+":
      return AddDisplay
    raise ValueError("%s is not a binary operator" % (op,))

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

  def enterExprs(self, ctx):
    self.PushStack()

  def exitExprs(self, ctx):
    self.Push(self.PopStack())

  def enterExprPairs(self, ctx):
    self.PushStack()

  def exitExprPairs(self, ctx):
    self.Push(self.PopStack())

  def exitNumExpr(self, ctx):
    self.Push(NumDisplay(ctx.atom.text))

  def exitStrExpr(self, ctx):
    self.Push(StrDisplay(ctx.atom.text))

  def exitIdExpr(self, ctx):
    self.Push(IdDisplay(ctx.atom.text))

  def exitListExpr(self, ctx):
    self.Push(ListDisplay(self.Pop()))

  def exitCallExpr(self, ctx):
    args = self.Pop()
    f = self.Pop()
    self.Push(CallDisplay(f, args))

  def exitBinOpExpr(self, ctx):
    rhs = self.Pop()
    lhs = self.Pop()
    op = ctx.op.text
    self.Push(self.SelectBinOpDisplayClass(op)(lhs, rhs))


def main():
  inp = antlr4.FileStream(sys.argv[1])
  lexer = CclLexer.CclLexer(inp)
  stream = antlr4.CommonTokenStream(lexer)
  parser = CclParser.CclParser(stream)
  tree = parser.start()
  walker = antlr4.ParseTreeWalker()
  listener = Listener()
  walker.walk(listener, tree)
  ctx = Context()
  ctx.Update({
      "nil": Nil(),
      "true": Bool(True),
      "false": Bool(False),
      "Print": Builtin(print),
      "Range": Builtin(range),
      "Dict": Builtin(Dict),
  })
  listener.result.Eval(ctx)

if __name__ == "__main__":
  main()
