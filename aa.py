import json
import sys

import antlr4

import AaListener
import AaLexer
import AaParser

JAVA_FUNC_TEMPLATE = '(new Function(){public Object call(Object... args){%s}})'
JAVA_CALL_TEMPLATE = JAVA_FUNC_TEMPLATE + '.call()'

class BaseListener(AaListener.AaListener):

  def Result(self, x):
    return x

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
    self.result = self.Result(self.stack[0][0])

  def enterSs(self, ctx):
    self.PushStack()
  def exitSs(self, ctx):
    self.Push(self.Block(self.PopStack()))

  ### Statement/Expression hybrids

  def enterB(self, ctx):
    self.PushStack()
  def exitB(self, ctx):
    self.Push(self.Scope(self.Block(self.PopStack())))

  def enterIfElse(self, ctx):
    self.PushStack()
  def exitIfElse(self, ctx):
    self.Push(self.If(*self.PopStack()))

  def enterIf(self, ctx):
    self.PushStack()
  def exitIf(self, ctx):
    self.Push(self.If(*(self.PopStack() + [self.Float(0.0)])))

  def enterWhile(self, ctx):
    self.PushStack()
  def exitWhile(self, ctx):
    self.Push(self.While(*self.PopStack()))

  ### Expressions

  def exitStr(self, ctx):
    self.Push(self.Str(''.join(eval(s.getText()) for s in ctx.STR())))

  def exitFloat(self, ctx):
    self.Push(self.Float(float(ctx.FLOAT().getText())))

  def exitInt(self, ctx):
    self.Push(self.Int(int(ctx.INT().getText())))

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

  def exitAttr(self, ctx):
    self.Push(self.Call(self.Name('__getitem__'), [self.Pop(), self.Str(ctx.NAME().getText())]))

  def enterCall(self, ctx):
    self.PushStack()
  def exitCall(self, ctx):
    # f, *args = self.PopStack() # Unfortunately doesn't work in Python2
    stack = self.PopStack()
    f = stack[0]
    args = stack[1:]
    self.Push(self.Call(f, args))

  def enterGetItem(self, ctx):
    self.PushStack()
  def exitGetItem(self, ctx):
    self.Push(self.Call(self.Name('__getitem__'), self.PopStack()))

  def exitDecl(self, ctx):
    self.Push(self.Decl(ctx.NAME().getText(), self.Pop()))

  def exitAssign(self, ctx):
    self.Push(self.Assign(ctx.NAME().getText(), self.Pop()))

  def enterAttrAssign(self, ctx):
    self.PushStack()

  def exitAttrAssign(self, ctx):
    e, value = self.PopStack()
    self.Push(self.Call(self.Name('__setitem__'), [e, self.Str(ctx.NAME().getText()), value]))

  def enterSetItem(self, ctx):
    self.PushStack()
  def exitSetItem(self, ctx):
    self.Push(self.Call(self.Name('__setitem__'), self.PopStack()))

  def exitLambda(self, ctx):
    v = ctx.var.getText() if ctx.var is not None else '_'
    self.Push(self.Lambda([n.getText() for n in ctx.NAME()], v, self.Pop()))

class ToTreeListener(BaseListener):

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

  def Float(self, s):
    return {'type': 'float', 'value': s}

  def Int(self, s):
    return {'type': 'int', 'value': s}

  def Name(self, s):
    return {'type': 'name', 'value': s}

  def Call(self, f, args):
    return {'type': 'call', 'f': f, 'args': args}

  def Decl(self, name, value):
    return {'type': 'decl', 'name': name, 'value': value}

  def Assign(self, name, value):
    return {'type': 'assign', 'name': name, 'value': value}

  def Lambda(self, names, varargs, body):
    return {'type': 'lambda', 'names': names, 'varargs': varargs, 'body': body}

class ToJavaListener(BaseListener):
  """
  Scope must provide
    boolean truthy(Object)
    Scope
    Context ctx
      void push()
      void push(Scope)
      Scope pop()
      Scope peek()
      Object get(String)
      Object declare(String, Object)
      Object assign(String, Object)
  """

  def __init__(self, name, base):
    self.name = name
    self.base = base

  def Result(self, x):
    return """
class %s extends %s {
    public static Object run(Context ctx) {
        Context outside;
        return %s;
    }
    public static void main(String[] args) {
        run(new Context());
    }
}
""" % (self.name, self.base, x)

  def Scope(self, body):
    return JAVA_CALL_TEMPLATE % 'ctx.push();Object r=%s;ctx.pop();return r;' % body

  def Block(self, stmts):
    return JAVA_CALL_TEMPLATE % '%s;return %s;' % (';'.join(stmts[:-1]), stmts[-1]) if stmts else '0'

  def If(self, cond, a, b):
    return 'truthy(%s) ? %s : %s' % (cond, a, b)

  def While(self, cond, body):
    return JAVA_CALL_TEMPLATE % 'Object r=0;while(truthy(%s))r=%s;return r;' % (cond, body)

  def Str(self, s):
    return '"%s"' % ''.join('\\u%04x' % ord(c) for c in s)

  def Float(self, s):
    return str(s)

  def Int(self, s):
    return str(s)

  def Name(self, s):
    return 'ctx.get(%s)' % self.Str(s)

  def Call(self, f, args):
    return '((Function)%s).call(%s)' % (f, ','.join(args))

  def Decl(self, name, value):
    return 'ctx.declare(%s, %s)' % (self.Str(name), value)

  def Assign(self, name, value):
    return 'ctx.assign(%s, %s)' % (self.Str(name), value)

  def Lambda(self, names, varargs, body):
    return JAVA_CALL_TEMPLATE % ''.join((
        'Scope save = ctx.peek();'
        ))
    return JAVA_FUNC_TEMPLATE % ''.join((
        'ctx.push();',
        ''.join('ctx.declare(%s,args[%d]);' % (n,i) for i, n in enumerate(names)),
        'Object varargs=new List();',
        'for (int i = %d; i < args.length; i++)varargs.add(args[i]);' % len(names),
        'ctx.declare(%s,varargs);' % varargs,
        'Object r=%s;' % body,
        'ctx.pop();return r;'))

def Parse(string, listener=None):
  listener = listener or ToTreeListener()
  inp = antlr4.InputStream.InputStream(string)
  lexer = AaLexer.AaLexer(inp)
  stream = antlr4.CommonTokenStream(lexer)
  parser = AaParser.AaParser(stream)
  tree = parser.start()
  walker = antlr4.ParseTreeWalker()
  walker.walk(listener, tree)
  return listener.result

def Main():
  cmd = sys.argv[1] if len(sys.argv) > 1 else 'json'
  string = sys.stdin.read()
  if cmd == 'json':
    print(json.dumps(Parse(string)))
  else:
    if cmd == 'java':
      name = sys.argv[2] if len(sys.argv) > 2 else 'AaProgram'
      base = sys.argv[3] if len(sys.argv) > 3 else 'BaseAaProgram'
      listener = ToJavaListener(name, base)
    else:
      raise ValueError(cmd + " is not a command")
    print(Parse(string, listener))

if __name__ == '__main__':
  Main()

