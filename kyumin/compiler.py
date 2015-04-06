"""Compiler that compiles ccl to json.

Originally I wanted to use just Python3, but kivy needs Python2.

Now I could write compiler.py in Python3 and then write vm.py
in Python2, but then I wouldn't be able to import constants from
compiler.py into vm.py.
"""

import json
import sys

import antlr4

from .grammar import KyuminListener
from .grammar import KyuminLexer
from .grammar import KyuminParser

SPECIALOPS = {'__list__', '__dict__', '__setitem__', '__getitem__'}

BINOP_TABLE = {
  '*': '__mul__',
  '/': '__truediv__',
  '//': '__floordiv__',
  '%': '__mod__',
  '+': '__add__',
  '-': '__sub__',

  '<': '__lt__',
  '<=': '__le__',
  '>': '__gt__',
  '>=': '__ge__',
}

### Statement/Expression hybrids

def Block(stmts, scope):
  return {'type': 'block', 'stmts': stmts, 'scope':int(scope)}

### Statements

def If(cond, a, b):
  return {'type': 'if', 'cond': cond, 'a': a, 'b': b}

def While(cond, body):
  return {'type': 'while', 'cond': cond, 'body': body}

### Expressions

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

def Decl(name, value):
  return {'type': 'decl', 'name': name, 'value': value}

def Assign(name, value):
  return {'type': 'assign', 'name': name, 'value': value}

def Lambda(names, varargs, body):
  return {'type': 'lambda', 'names': names, 'varargs': varargs, 'body': body}

class Listener(KyuminListener.KyuminListener):

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
    self.Push(Block(self.PopStack(), False))

  ### Statement/Expression hybrids

  def enterB(self, ctx):
    self.PushStack()
  def exitB(self, ctx):
    self.Push(Block(self.PopStack(), True))

  ### Statements

  def enterIfElse(self, ctx):
    self.PushStack()
  def exitIfElse(self, ctx):
    self.Push(If(*self.PopStack()))

  def enterIf(self, ctx):
    self.PushStack()
  def exitIf(self, ctx):
    self.Push(If(*(self.PopStack() + [Int(0)])))

  def enterWhile(self, ctx):
    self.PushStack()
  def exitWhile(self, ctx):
    self.Push(While(*self.PopStack()))

  ### Expressions

  def exitStr(self, ctx):
    self.Push(Str(eval(ctx.STR().getText())))

  def exitFloat(self, ctx):
    self.Push(Float(float(ctx.FLOAT().getText())))

  def exitInt(self, ctx):
    self.Push(Int(int(ctx.INT().getText())))

  def exitName(self, ctx):
    self.Push(Name(ctx.NAME().getText()))

  def enterList(self, ctx):
    self.PushStack()
  def exitList(self, ctx):
    self.Push(Call(Name('__list__'), self.PopStack()))

  def enterDict(self, ctx):
    self.PushStack()
  def exitDict(self, ctx):
    self.Push(Call(Name('__dict__'), self.PopStack()))

  def exitAttr(self, ctx):
    self.Push(Call(Name('__getitem__'), [self.Pop(), Str(ctx.NAME().getText())]))

  def enterCall(self, ctx):
    self.PushStack()
  def exitCall(self, ctx):
    # f, *args = self.PopStack() # Unfortunately doesn't work in Python2
    stack = self.PopStack()
    f = stack[0]
    args = stack[1:]
    self.Push(Call(f, args))

  def enterGetItem(self, ctx):
    self.PushStack()
  def exitGetItem(self, ctx):
    self.Push(Call(Name('__getitem__'), self.PopStack()))

  def enterBinop(self, ctx):
    self.PushStack()
  def exitBinop(self, ctx):
    self.Push(Call(Name(BINOP_TABLE[ctx.op.text]), self.PopStack()))

  def exitDecl(self, ctx):
    self.Push(Decl(ctx.NAME().getText(), self.Pop()))

  def exitAssign(self, ctx):
    self.Push(Assign(ctx.NAME().getText(), self.Pop()))

  def enterAttrAssign(self, ctx):
    self.PushStack()

  def exitAttrAssign(self, ctx):
    e, value = self.PopStack()
    self.Push(Call(Name('__setitem__'), [e, Str(ctx.NAME().getText()), value]))

  def enterSetItem(self, ctx):
    self.PushStack()
  def exitSetItem(self, ctx):
    self.Push(Call(Name('__setitem__'), self.PopStack()))

  def exitLambda(self, ctx):
    v = ctx.var.getText() if ctx.var is not None else '_'
    self.Push(Lambda([n.getText() for n in ctx.NAME()], v, self.Pop()))

def _Parse(source, fromfile, throw):
    inpcls = antlr4.FileStream if fromfile else antlr4.InputStream.InputStream
    inp = inpcls(source)
    lexer = KyuminLexer.KyuminLexer(inp)
    stream = antlr4.CommonTokenStream(lexer)
    parser = KyuminParser.KyuminParser(stream)
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
