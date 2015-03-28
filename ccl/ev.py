import os

from . import display


class Context(object):

  def __init__(self, parent=None, table=None):
    self.parent = parent
    self.table = table or dict()

  def __getitem__(self, name):
    if name in self.table:
      return self.table[name]
    elif self.parent is not None:
      return self.parent[name]
    else:
      raise KeyError(name)

  def __setitem__(self, name, value):
    if name in self.table:
      self.table[name] = value
    elif self.parent is not None:
      self.parent[name] = value
    else:
      raise KeyError(name)

  def Declare(self, name, value):
    self.table[name] = value

  def Keys(self):
    if self.parent is None:
      return list(self.table.keys())
    else:
      return list(set(self.table.keys()) | set(self.parent.Keys()))


class Obj(object):

  def __repr__(self):
    return str(self)


class Str(Obj, str):

  def __repr__(self):
    return str.__repr__(self)


class List(Obj, list):

  def __hash__(self):
    return hash(tuple(self))

  def __str__(self):
    return '[%s]' % ' '.join(map(repr, self))


class Dict(Obj, dict):

  def __hash__(self):
    return hash(frozenset(self.items()))

  def __str__(self):
    return '[%s]' % ' '.join('%r:%r' % pair for pair in self.items())


class Lambda(Obj, display.NamedTuple('names body ctx')):

  def __call__(self, *args):
    ctx = Context(self.ctx)

    for name, arg in zip(self.names, args):
      ctx.Declare(name, arg)

    return Eval(ctx, self.body)

  def __str__(self):
    return '<lambda>'


class Builtin(Obj, display.NamedTuple('name f')):

  def __call__(self, *args):
    return Convert(self.f(*args))

  def __str__(self):
    return '<builtin %s>' % self.name


def Convert(value):
  if isinstance(value, Obj):
    return value
  elif value is None:
    return Str(0)
  elif isinstance(value, (int, float, str)):
    return Str(value)
  elif isinstance(value, (list, tuple)):
    return List(Convert(item) for item in value)
  elif isinstance(value, dict):
    return Dict((Convert(k), Convert(v)) for k, v in value.items())
  else:
    raise ValueError((type(result), result))


def Revert(value):
  if not isinstance(value, Obj):
    return value
  elif isinstance(value, Str):
    try:
      return int(value)
    except ValueError:
      try:
        f = float(value)
        return int(f) if f == int(f) else f
      except ValueError:
        return str(value)
  elif isinstance(value, List):
    return [Revert(item) for item in value]
  elif isinstance(value, Dict):
    return {Revert(k):Revert(v) for k, v in value.items()}
  assert False, (type(value), value)


def Eval(ctx, d):
  if isinstance(d, (display.Stmts, display.Block)):
    if isinstance(d, display.Block):
      ctx = Context(ctx)
    last = Str(0)
    for d in d:
      last = Eval(ctx, d)
    return last
  elif isinstance(d, display.Call):
    f = Eval(ctx, d.f)
    if isinstance(f, Str):
      f = ctx[f]
    args = [Eval(ctx, arg) for arg in d.args]
    return f(*args)
  elif isinstance(d, display.IfElse):
    return Eval(ctx, (d.a if Eval(ctx, d.cond) else d.b))
  elif isinstance(d, display.If):
    return Eval(ctx, d.body) if Eval(ctx, d.cond) else Str(0)
  elif isinstance(d, display.While):
    last = Str(0)
    while Eval(ctx, d.cond):
      last = Eval(ctx, d.body)
    return last
  elif isinstance(d, display.Decl):
    ctx.Declare(d.name, Eval(ctx, d.value))
    return Str(0)
  elif isinstance(d, display.Assign):
    ctx[d.name] = Eval(ctx, d.value)
    return Str(0)
  elif isinstance(d, display.Str):
    return Str(d)
  elif isinstance(d, display.Var):
    return ctx[str(d)]
  elif isinstance(d, display.Lambda):
    return Lambda(d.names, d.body, ctx)
  elif isinstance(d, display.List):
    return List(Eval(ctx, item) for item in d)
  elif isinstance(d, display.Dict):
    return Dict((Eval(ctx, key), Eval(ctx, value)) for key, value in d)
  else:
    raise ValueError((type(d), d))
  assert False, type(d)


GLOBAL = Context(None, {
  'just': Builtin('just', lambda x: x),

  'echo': Builtin('echo', lambda x: (print(x), x)[-1]),
  'ls': Builtin('ls', os.listdir),

  '..': Builtin('..', lambda a, b: a + b),
  '.*': Builtin('.*', lambda s, n: s * int(n)),

  '+': Builtin('+', lambda a, b: Revert(a) + Revert(b)),
  '-': Builtin('-', lambda a, b: Revert(a) - Revert(b)),
  '*': Builtin('*', lambda a, b: Revert(a) * Revert(b)),
  '/': Builtin('/', lambda a, b: Revert(a) / Revert(b)),
  '//': Builtin('//', lambda a, b: Revert(a) // Revert(b)),
})

