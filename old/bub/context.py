import os
import sys
import urllib.request

from . import value


def BuiltinPrint(*args):
  print(*args)
  return args[-1] if args else None


def BuiltinExpand(path):
  return os.path.expandvars(os.path.expanduser(path))


def BuiltinLs(path='.'):
  return os.listdir(BuiltinExpand(path))


def BuiltinCd(path='~'):
  os.chdir(BuiltinExpand(path))


def BuiltinCat(path):
  with open(path) as f:
    return f.read()


def BuiltinGet(url):
  with urllib.request.urlopen(url) as f:
    return f.read().decode('utf-8')


def BuiltinLessThan(lhs, rhs):
  return lhs < rhs


def BuiltinAdd(lhs, rhs):
  return lhs + rhs


def BuiltinSubtract(lhs, rhs):
  return lhs - rhs


GLOBAL = value.Context(None, {
  'nil': value.Nil(),
  'true': value.Bool(1),
  'false': value.Bool(0),

  'print': value.Builtin('print', BuiltinPrint),
  'just': value.Builtin('just', lambda x : x),

  'len': value.Builtin('len', len),

  'ls': value.Builtin('ls', BuiltinLs),
  'cd': value.Builtin('cd', BuiltinCd),
  'cat': value.Builtin('cat', BuiltinCat),

  'get': value.Builtin('get', BuiltinGet),

  'lt': value.Builtin('lt', BuiltinLessThan),

  '+': value.Builtin('+', BuiltinAdd),
  '-': value.Builtin('-', BuiltinSubtract),
})
