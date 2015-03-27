from . import value
from . import utils


class Display(object):
  pass


class Block(tuple, Display):

  def Eval(self, ctx, new_scope=True):
    bctx = value.Context(ctx) if new_scope else ctx
    last = value.Nil()
    for d in self:
      last = d.Eval(bctx)
    return last


class Call(utils.NamedTuple('f args kwargs'), Display):

  def Eval(self, ctx):
    f = self.f.Eval(ctx)
    args = [arg.Eval(ctx) for arg in self.args]
    kwargs = {k:arg.Eval(ctx) for k, arg in self.kwargs.items()}
    return f(*args, **kwargs)


class While(utils.NamedTuple('cond body'), Display):

  def Eval(self, ctx):
    last = value.Nil()
    while self.cond.Eval(ctx):
      last = self.body.Eval(ctx)
    return last


class Declaration(utils.NamedTuple('name value'), Display):

  def Eval(self, ctx):
    value = self.value.Eval(ctx)
    ctx.Declare(self.name, value)
    return value


class Assignment(utils.NamedTuple('name value'), Display):

  def Eval(self, ctx):
    value = self.value.Eval(ctx)
    ctx[self.name] = value
    return value


class Lambda(utils.NamedTuple('args body'), Display):

  def Eval(self, ctx):
    return value.Lambda(self.args, self.body, ctx)


class Num(str, Display):

  def Eval(self, ctx):
    return value.Num(self)


class Str(str, Display):

  def Eval(self, ctx):
    return value.Str(eval(self))


class Id(str, Display):

  def Eval(self, ctx):
    return ctx[self]
