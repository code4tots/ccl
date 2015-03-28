import sys

import antlr4

from . import display
from .grammar import CclListener
from .grammar import CclLexer
from .grammar import CclParser


class Listener(CclListener.CclListener):

    def PushStack(self):
        self.stack.append([])

    def PopStack(self):
        return self.stack.pop()

    def Push(self, value):
        self.stack[-1].append(value)

    def Pop(self):
        return self.stack[-1].pop()

    def enterStart(self, ctx):
        self.stack = [[]]

    def exitStart(self, ctx):
        assert len(self.stack) == 1, self.stack
        assert len(self.stack[0]) == 1, self.stack[0]
        self.result = self.stack[0][0]

    def enterStmts(self, ctx):
        self.PushStack()

    def exitStmts(self, ctx):
        self.Push(display.Block(self.PopStack()))

    def enterCall(self, ctx):
        self.PushStack()

    def exitCall(self, ctx):
        f, *args = self.PopStack()
        self.Push(display.Call(f, args))

    def exitIfElse(self, ctx):
        b = self.Pop()
        a = self.Pop()
        cond = self.Pop()
        self.Push(display.IfElse(cond, a, b))

    def exitIf(self, ctx):
        body = self.Pop()
        cond = self.Pop()
        self.Push(display.If(cond, body))

    def exitWhile(self, ctx):
        body = self.Pop()
        cond = self.Pop()
        self.Push(display.While(cond, body))

    def exitDecl(self, ctx):
        name = ctx.STR().getText()
        value = self.Pop()
        self.Push(display.Decl(name, value))

    def exitAssign(self, ctx):
        name = ctx.STR().getText()
        value = self.Pop()
        self.Push(display.Assign(name, value))

    def exitStr(self, ctx):
        name = ctx.STR().getText()
        if name.startswith(('"', "'")):
            name = eval(name)
        self.Push(display.Str(name))

    def exitVar(self, ctx):
        name = ctx.VAR().getText()
        assert name.startswith('$')
        self.Push(display.Var(name[1:]))

    def exitLambda(self, ctx):
        names = [tok.getText() for tok in ctx.STR()]
        body = self.Pop()
        self.Push(display.Lambda(names, body))

    def enterList(self, ctx):
        self.PushStack()

    def exitList(self, ctx):
        self.Push(display.List(self.PopStack()))

    def enterDict(self, ctx):
        self.PushStack()

    def exitDict(self, ctx):
        exprs = self.PopStack()
        self.Push(display.Dict(zip(exprs[::2], exprs[1::2])))


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
        return display.Stmts(_Parse(source, fromfile, True))
    except antlr4.error.Errors.ParseCancellationException:
        _Parse(source, fromfile, False)
        return


if __name__ == '__main__':
    disp = Parse(sys.stdin.read())
    if disp is not None:
        print(disp)
