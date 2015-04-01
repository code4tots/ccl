import json
import sys

from . import compiler
from . import vm


def Run(string, ctx=None):
  return vm.Eval(compiler.Parse(string), ctx or vm.Context(vm.GLOBAL))


if __name__ == '__main__':
  Run(sys.stdin.read())
