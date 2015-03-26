import antlr4

from . import display
from . import utils
from .grammar import BubListener
from .grammar import BubLexer
from .grammar import BubParser


class Listener(BubListener.BubListener):

  def __init__(self):
    self.stack = None

  @property
  def result(self):
    return self.stack[0][0]

  def PushStack(self):
    self.stack.append([])

  def PopStack(self):
    return self.stack.pop()

  def Push(self, value):
    self.stack[-1].append(value)

  def Pop(self):
    return self.stack[-1].pop()


  @utils.overrides(BubListener.BubListener)
  def enterStart(self, ctx):
      self.stack = [[]]

  @utils.overrides(BubListener.BubListener)
  def exitStart(self, ctx):
      assert len(self.stack) == 1, self.stack
      assert len(self.stack[0]) == 1, self.stack[0]


  @utils.overrides(BubListener.BubListener)
  def enterStmts(self, ctx):
      self.PushStack()

  @utils.overrides(BubListener.BubListener)
  def exitStmts(self, ctx):
      self.Push(display.Block(self.PopStack()))


  @utils.overrides(BubListener.BubListener)
  def enterStmt(self, ctx):
    pass

  @utils.overrides(BubListener.BubListener)
  def exitStmt(self, ctx):
    pass


  @utils.overrides(BubListener.BubListener)
  def enterCall(self, ctx):
    self.PushStack()

  @utils.overrides(BubListener.BubListener)
  def exitCall(self, ctx):
    self.Push(display.Call(self.PopStack()))


  @utils.overrides(BubListener.BubListener)
  def enterBlock(self, ctx):
    pass

  @utils.overrides(BubListener.BubListener)
  def exitBlock(self, ctx):
    pass


  @utils.overrides(BubListener.BubListener)
  def enterIfElse(self, ctx):
    pass

  @utils.overrides(BubListener.BubListener)
  def exitIfElse(self, ctx):
    b = self.Pop()
    a = self.Pop()
    cond = self.Pop()
    self.Push(display.IfElse(cond, a, b))


  @utils.overrides(BubListener.BubListener)
  def enterIf(self, ctx):
    pass

  @utils.overrides(BubListener.BubListener)
  def exitIf(self, ctx):
    body = self.Pop()
    cond = self.Pop()
    self.Push(display.If(cond, body))


  @utils.overrides(BubListener.BubListener)
  def enterWhile(self, ctx):
    pass

  @utils.overrides(BubListener.BubListener)
  def exitWhile(self, ctx):
    body = self.Pop()
    cond = self.Pop()
    self.Push(display.While(cond, body))


  @utils.overrides(BubListener.BubListener)
  def enterDeclaration(self, ctx):
    pass

  @utils.overrides(BubListener.BubListener)
  def exitDeclaration(self, ctx):
    expr = self.Pop()
    self.Push(display.Declaration(ctx.ID().getText(), expr))


  @utils.overrides(BubListener.BubListener)
  def enterAssignment(self, ctx):
    pass

  @utils.overrides(BubListener.BubListener)
  def exitAssignment(self, ctx):
    expr = self.Pop()
    self.Push(display.Assignment(ctx.ID().getText(), expr))


  @utils.overrides(BubListener.BubListener)
  def enterNum(self, ctx):
    pass

  @utils.overrides(BubListener.BubListener)
  def exitNum(self, ctx):
    self.Push(display.Num(ctx.NUM.getText()))


  @utils.overrides(BubListener.BubListener)
  def enterStr(self, ctx):
    pass

  @utils.overrides(BubListener.BubListener)
  def exitStr(self, ctx):
    self.Push(display.Str(ctx.STR.getText()))


  @utils.overrides(BubListener.BubListener)
  def enterId(self, ctx):
    pass

  @utils.overrides(BubListener.BubListener)
  def exitId(self, ctx):
    self.Push(display.Id(ctx.ID().getText()))


  @utils.overrides(BubListener.BubListener)
  def enterLambda(self, ctx):
    self.PushStack()

  @utils.overrides(BubListener.BubListener)
  def exitLambda(self, ctx):
    body = self.Pop()
    args = self.PopStack()
    self.Push(display.Lambda(args, body))


  @utils.overrides(BubListener.BubListener)
  def enterList(self, ctx):
    self.PushStack()

  @utils.overrides(BubListener.BubListener)
  def exitList(self, ctx):
    self.Push(display.List(self.PopStack()))


  @utils.overrides(BubListener.BubListener)
  def enterDict(self, ctx):
    self.PushStack()

  @utils.overrides(BubListener.BubListener)
  def exitDict(self, ctx):
    exprs = self.PopStack()
    self.Push(display.Dict(exprs[::2], exprs[1::2]))


  @utils.overrides(BubListener.BubListener)
  def enterCmdExpr(self, ctx):
    pass

  @utils.overrides(BubListener.BubListener)
  def exitCmdExpr(self, ctx):
    pass


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

