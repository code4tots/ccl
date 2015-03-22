import datetime
import os

from . import context
from . import value
from . import run


def Repl():
  ctx = value.Context(context.GLOBAL)

  try:
    while True:
      prompt = '%s %s$ ' % (datetime.datetime.now(), os.getcwd().split('/')[-1])
      result = run.Run(input(prompt), ctx)
      if result is not value.Nil():
        print(result)
  except EOFError:
    print()


if __name__ == '__main__':
  Repl()
