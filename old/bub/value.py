from . import utils


def Convert(x):
  if isinstance(x, Object):
    return x

  elif x is None:
    return Nil()

  elif isinstance(x, bool):
    return Bool(x)

  elif isinstance(x, (int, float)):
    return Num(x)

  elif isinstance(x, str):
    return Str(x)

  elif isinstance(x, (list, tuple)):
    return List(map(Object.Convert(x)))

  elif isinstance(x, dict):
    return Dict((Convert(k), Convert(v)) for k, v in x.items())

  raise ValueError("Can't convert object of type '%s'" % type(x))


class Object(object):

  def __repr__(self):
    return self.__str__()


class Nil(Object):
  _instance = None

  def __new__(cls):
    if cls._instance is None:
      cls._instance = super(Nil, cls).__new__(cls)

    return cls._instance

  def __str__(self):
    return 'nil'

  def __bool__(self):
    return False


class Bool(int, Object):

  def __str__(self):
    return 'true' if self else 'false'


class Num(float, Object):

  def __str__(self):
    return str((int if int(self) == self else float)(self))


class Str(str, Object):
  pass


class List(list, Object):

  def __hash__(self):
    return hash(tuple(self))


class Dict(dict, Object):

  def __hash__(self):
    return hash(frozenset(self.items()))


class Lambda(utils.NamedTuple('args body ctx'), Object):

  def __call__(self, *args):
    ctx = Context(ctx)
    for name, value in zip(self.args, args):
      ctx.Declare(name, value)
    return self.body.Eval(ctx)


class Builtin(Object):

  def __init__(self, name, f):
    self.name = name
    self.f = f

  def __call__(self, *args, **kwargs):
    return Convert(self.f(*args, **kwargs))

  def __str__(self):
    return "<builtin '%s'>" % self.name


class Context(object):

  def __init__(self, parent=None, table=None):
    self.parent = parent
    self.table = table or dict()

  def __str__(self):
    return '(%s, %s)' % (self.table, self.parent)

  def __getitem__(self, key):
    if key in self.table:
      return self.table[key]

    if self.parent is None:
      raise KeyError('Variable %r not defined' % key)

    return self.parent[key]

  def __setitem__(self, key, value):
    assert isinstance(value, Object)
    if key in self.table:
      self.table[key] = value
    elif self.parent is None:
      raise KeyError('Variable %r not defined' % key)
    else:
      self.parent[key] = value

  def Declare(self, key, value):
    assert isinstance(value, Object)
    if key in self.table:
      raise ValueError('%r is already declared in this scope' % key)
    self.table[key] = value

  def Update(self, dict_):
    for key, value in dict_.items():
      self.Declare(key, value)
