import os
import sys

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


GLOBAL = value.Context(None, {
  'nil': value.Nil(),
  'true': value.Bool(1),
  'false': value.Bool(0),

  'print': value.Builtin('print', BuiltinPrint),
  'just': value.Builtin('just', lambda x : x),

  'ls': value.Builtin('ls', BuiltinLs),
  'cd': value.Builtin('cd', BuiltinCd),
})
