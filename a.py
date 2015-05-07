"""

ast types
  list
  int
  foat
  str

"""

import json
import sys

import antlr4

import AListener
import ALexer
import AParser


class Listener(AListener.AListener):

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
    self.result = ['block'] + self.stack.pop()

  def enterIfElse(self, ctx):
    self.PushStack()
  def exitIfElse(self, ctx):
    self.Push(['if'] + self.PopStack())

  def enterIf_(self, ctx):
    self.PushStack()
  def exitIf_(self, ctx):
    self.Push(['if'] + self.PopStack() + [0])

  def enterWhile(self, ctx):
    self.PushStack()
  def exitWhile(self, ctx):
    self.Push(['while'] + self.PopStack())

  def exitStr(self, ctx):
    self.Push(['quote'] + [''.join(str(eval(s.getText())) for s in ctx.STR())])

  def exitName(self, ctx):
    self.Push(ctx.NAME().getText())

  def enterC(self, ctx):
    self.PushStack()
  def exitC(self, ctx):
    self.Push(self.PopStack())

  def enterList(self, ctx):
    self.PushStack()
  def exitList(self, ctx):
    self.Push(['__list__'] + self.PopStack())

  def enterDict(self, ctx):
    self.PushStack()
  def exitDict(self, ctx):
    self.Push(['__dict__'] + self.PopStack())

  def exitLambda(self, ctx):
    self.Push(self.Lambda([n.getText() for n in ctx.NAME()], self.Pop()))


def Parse(string):
  parser = AParser.AParser(antlr4.CommonTokenStream(ALexer.ALexer(antlr4.InputStream.InputStream(string))))
  tree = parser.start()
  listener = Listener()
  antlr4.ParseTreeWalker().walk(listener, tree)
  if parser._syntaxErrors:
    return None
  return listener.result

if __name__ == '__main__':
  print(Parse(sys.stdin.read()))


