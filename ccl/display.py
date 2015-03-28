import collections


def NamedTuple(fields):
  return collections.namedtuple('NamedTuple', fields)


class Display(object):

  def __repr__(self):
    if isinstance(self, tuple):
      if hasattr(self, '_fields'):
        return super(Display, self).__repr__()
      else:
        return type(self).__name__ + super(Display, self).__repr__()
    else:
      assert isinstance(self, str), type(self)
      return type(self).__name__ + str.__repr__(self)


class Stmts(Display, tuple):
  pass


class Block(Display, tuple):
  pass


class Call(Display, NamedTuple('f args')):
  pass


class IfElse(Display, NamedTuple('cond a b')):
  pass


class If(Display, NamedTuple('cond body')):
  pass


class While(Display, NamedTuple('cond body')):
  pass


class Decl(Display, NamedTuple('name value')):
  pass


class Assign(Display, NamedTuple('name value')):
  pass


class Str(Display, str):
  pass


class Var(Display, str):
  pass


class Lambda(Display, NamedTuple('names body')):
  pass


class List(Display, tuple):
  pass


class Dict(Display, tuple):
  pass

