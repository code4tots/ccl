import antlr4

from . import display
from .grammar import BubLexer
from .grammar import BubListener
from .grammar import BubParser


class Listener(BubListener.BubListener):

  def __init__(self):
    self.stack = self.dstack = self.result = None

  def PushStack(self):
    self.stack.append([])

  def PopStack(self):
    return self.stack.pop()

  def PushDict(self):
    self.dstack.append(dict())

  def PopDict(self):
    return self.dstack.pop()

  def __setitem__(self, key, value):
    self.dstack[-1][key] = value

  def Push(self, value):
    self.stack[-1].append(value)

  def Pop(self):
    return self.stack[-1].pop()

  def enterStart(self, ctx):
    self.stack = [[]]
    self.dstack = []
    self.result = None

  def exitStart(self, ctx):
    assert len(self.stack) == 1
    assert len(self.stack[0]) == 1
    self.result = self.Pop()
    self.stack = None

  def enterStmts(self, ctx):
    self.PushStack()

  def exitStmts(self, ctx):
    self.Push(display.Block(self.PopStack()))

  def exitCall(self, ctx):
    args = self.PopStack()
    kwargs = self.PopDict()
    f = self.Pop()
    self.Push(display.Call(f, args, kwargs))

  def exitDeclaration(self, ctx):
    value = self.Pop()
    name = ctx.name.text
    self.Push(display.Declaration(name, value))

  def exitAssignment(self, ctx):
    value = self.Pop()
    name = ctx.name.text
    self.Push(display.Assignment(name, value))

  def exitNum(self, ctx):
    self.Push(display.Num(ctx.atom.text))

  def exitStr(self, ctx):
    self.Push(display.Str(ctx.atom.text))

  def exitId(self, ctx):
    self.Push(display.Id(ctx.atom.text))

  def enterArgs(self, ctx):
    self.PushStack()
    self.PushDict()

  def exitKwarg(self, ctx):
    self[ctx.name.text] = self.Pop()


def _Parse(source, fromfile, throw):
  inp = (antlr4.FileStream if fromfile else antlr4.InputStream.InputStream)(source)
  lexer = BubLexer.BubLexer(inp)
  stream = antlr4.CommonTokenStream(lexer)
  parser = BubParser.BubParser(stream)
  if throw:
    parser._errHandler = antlr4.BailErrorStrategy()
  tree = parser.start()
  walker = antlr4.ParseTreeWalker()
  listener = Listener()
  walker.walk(listener, tree)
  return listener.result


def Parse(source, fromfile=False):
  # TODO: better error handling.
  try:
    return _Parse(source, fromfile, True)
  except antlr4.error.Errors.ParseCancellationException:
    pass
