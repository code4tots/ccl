from . import utils


class Display(object):

  def __str__(self):
    return '%s(%s)' % (type(self).__name__, super(Display, self).__str__())

  def __repr__(self):
    return '%s(%s)' % (type(self).__name__, super(Display, self).__repr__())


class Block(Display, tuple):
  pass


class Call(Display, tuple):
  pass


class IfElse(Display, utils.NamedTuple('cond a b')):
  pass


class If(Display, utils.NamedTuple('cond body')):
  pass


class While(Display, utils.NamedTuple('cond body')):
  pass


class Declaration(Display, utils.NamedTuple('name value')):
  pass


class Assignment(Display, utils.NamedTuple('name value')):
  pass


class Num(Display, str):
  pass


class Str(Display, str):
  pass


class Id(Display, str):
  pass


class Lambda(Display, utils.NamedTuple('args body')):
  pass


class List(Display, tuple):
  pass


class Dict(Display, tuple):
  pass



