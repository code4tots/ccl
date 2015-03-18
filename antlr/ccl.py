# Uses python3 version of antlr

import collections
import sys

import antlr4

import CclLexer
import CclListener
import CclParser


def NamedTuple(attrs):
  return collections.namedtuple("namedtuple", attrs)


class Context(object):

  def __init__(self, parent=None):
    self.table = dict()
    self.parent = parent

  def __getitem__(self, name):
    return self.table[name] if name in self.table else self.parent[name]

  def __setitem__(self, name, value):
    (self.table if name in self.table else self.parent)[name] = value


class Display(object):
  pass


class NumDisplay(str, Display):

  def Eval(self, ctx):
    return float(self)


class IdDisplay(str, Display):

  def Eval(self, ctx):
    return ctx[str(self)]


class MulDisplay(NamedTuple("lhs rhs"), Display):

  def Eval(self, ctx):
    lhs, rhs = (d.Eval(ctx) for d in self)
    return lhs * rhs


class CallDisplay(NamedTuple("f args"), Display):

  def Eval(self, ctx):
    f = self[0].Eval(ctx)
    args = [d.Eval(ctx) for d in self[1]]
    return f(*args)


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

  def exitIntExpr(self, ctx):
    self.Push(NumDisplay(ctx.atom.text))

  def exitIdExpr(self, ctx):
    self.Push(IdDisplay(ctx.atom.text))

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
  ctx.table["print"] = print
  print(listener.result)
  listener.result.Eval(ctx)

if __name__ == "__main__":
  main()
