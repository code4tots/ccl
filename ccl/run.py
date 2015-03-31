import sys

from . import compiler
from . import vm


def Run(string, ctx=None):
  return vm.Eval(compiler.Parse(string), ctx)


if __name__ == '__main__':
  return Run(sys.stdin.read())
