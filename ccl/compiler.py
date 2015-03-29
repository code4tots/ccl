import json
import sys

import antlr4

from .grammar import CclListener
from .grammar import CclLexer
from .grammar import CclParser

def Str(s):
  return {'type': 'str', 'value': s}

def Float(s):
  return {'type': 'float', 'value': s}

def Int(s):
  return {'type': 'int', 'value': s}

def Name(s):
  return {'type': 'name', 'value': s}

def Call(f, args):
  return {'type': 'call', 'f': f, 'args': args}

def Block(statements, scope=True):
  return {'type': 'block', 'statements': statements, 'scope':int(scope)}

class Listener(CclListener.CclListener):

  def Push(self, value):
    self.stack[-1].append(value)

  def Pop(self):
    return self.stack[-1].pop()

  def PushStack(self):
    self.stack.append([])

  def PopStack(self):
    return self.stack.pop()

  def enterStart(self, ctx):
    self.stack = [[]]

  def exitStart(self, ctx):
    assert len(self.stack) == 1, self.stack
    assert len(self.stack[0]) == 1, self.stack[0]
    self.result = self.stack[0][0]

  def enterSs(self, ctx):
    self.PushStack()

  def exitSs(self, ctx):
    self.Push(Block(self.PopStack(), scope=False))

  ### Expressions

  def exitStr(self, ctx):
    self.Push(Str(ctx.STR().getText()))

  def exitFloat(self, ctx):
    self.Push(Float(ctx.FLOAT().getText()))

  def exitInt(self, ctx):
    self.Push(Int(ctx.INT().getText()))

  def exitName(self, ctx):
    self.Push(Name(ctx.NAME().getText()))

  def enterCall(self, ctx):
    self.PushStack()

  def exitCall(self, ctx):
    f, *args = self.PopStack()
    self.Push(Call(f, args))


def _Parse(source, fromfile, throw):
    inpcls = antlr4.FileStream if fromfile else antlr4.InputStream.InputStream
    inp = inpcls(source)
    lexer = CclLexer.CclLexer(inp)
    stream = antlr4.CommonTokenStream(lexer)
    parser = CclParser.CclParser(stream)
    if throw:
        parser._errHandler = antlr4.BailErrorStrategy()
    tree = parser.start()
    walker = antlr4.ParseTreeWalker()
    listener = Listener()
    walker.walk(listener, tree)
    return listener.result

def Parse(source, fromfile=False):
    try:
        return _Parse(source, fromfile, True)
    except antlr4.error.Errors.ParseCancellationException:
        _Parse(source, fromfile, False)
        return

if __name__ == '__main__':
  print(json.dumps(Parse(sys.stdin.read())))
