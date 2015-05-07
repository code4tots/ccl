import json
import sys

import antlr4

import CclListener
import CclLexer
import CclParser

class BaseListener(CclListener.CclListener):

  def Finalize(self, result):
    return result

  def Push(self, value):
    self.stack[-1].append(value)

  def MultiPop(self, n):
    items = self.stack[-1][-n:]
    del self.stack[-1][-n:]
    return items

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
    self.result = self.Finalize(self.Block(self.stack.pop()))

  def enterB(self, ctx):
    self.PushStack()
  def exitB(self, ctx):
    return self.Push(self.Scope(self.Block(self.PopStack())))

  def enterIfElse(self, ctx):
    self.PushStack()
  def exitIfElse(self, ctx):
    self.Push(self.If(*self.PopStack()))

  def enterWhile(self, ctx):
    self.PushStack()
  def exitWhile(self, ctx):
    self.Push(self.While(*self.PopStack()))

  def exitStr(self, ctx):
    self.Push(self.Str(''.join(str(eval(s.getText())) for s in ctx.STR())))

  def exitName(self, ctx):
    self.Push(self.Name(ctx.NAME().getText()))

  def enterList(self, ctx):
    self.PushStack()
  def exitList(self, ctx):
    self.Push(self.Call(self.Name('__list__'), self.PopStack()))

  def enterDict(self, ctx):
    self.PushStack()
  def exitDict(self, ctx):
    self.Push(self.Call(self.Name('__dict__'), self.PopStack()))

  def enterCall(self, ctx):
    self.PushStack()
  def exitCall(self, ctx):
    fargs = self.PopStack()
    f, args = fargs[0], fargs[1:]
    self.Push(self.Call(f, args))

  def exitGetItem(self, ctx):
    self.Push(self.Call(self.Name('__getitem__'), self.MultiPop(2)))

  def exitSetItem(self, ctx):
    self.Push(self.Call(self.Name('__setitem__'), self.MultiPop(3)))

  def exitAssign(self, ctx):
    self.Push((self.Assign if ctx.op.text == '=' else self.Decl)(ctx.NAME().getText(), self.Pop()))

  def exitLambda(self, ctx):
    self.Push(self.Lambda([n.getText() for n in ctx.NAME()], self.Pop()))

class ToDictListener(BaseListener):

  def Scope(self, body):
    return {'type': 'scope', 'body': body}

  def Block(self, stmts):
    return {'type': 'block', 'stmts': stmts}

  def If(self, cond, a, b):
    return {'type': 'if', 'cond': cond, 'a': a, 'b': b}

  def While(self, cond, body):
    return {'type': 'while', 'cond': cond, 'body': body}

  def Str(self, s):
    return {'type': 'str', 'value': s}

  def Name(self, s):
    return {'type': 'name', 'value': s}

  def Call(self, f, args):
    return {'type': 'call', 'f': f, 'args': args}

  def Decl(self, name, value):
    return {'type': 'decl', 'name': name, 'value': value}

  def Assign(self, name, value):
    return {'type': 'assign', 'name': name, 'value': value}

  def Lambda(self, names, body):
    return {'type': 'lambda', 'names': names, 'body': body}

class ToJsonListener(ToDictListener):

  def Finalize(self, x):
    return json.dumps(x)

def Parse(string, listener=None):
  tree = CclParser.CclParser(antlr4.CommonTokenStream(CclLexer.CclLexer(antlr4.InputStream.InputStream(string)))).start()
  listener = listener or ToDictListener()
  antlr4.ParseTreeWalker().walk(listener, tree)
  return listener.result

if __name__ == '__main__':
  print(Parse(sys.stdin.read(), ToJsonListener()))

