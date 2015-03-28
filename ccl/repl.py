import datetime
import os
import readline
import traceback

from . import ev
from . import parser


readline.parse_and_bind('tab: complete')
readline.parse_and_bind('set editing-mode emacs')


class Completer(object):

  def __init__(self, ctx):
    self.ctx = ctx
    self.completions = None

  def Complete(self, text):
    # Strange... text doesn't give me the entire line, but only the
    # most recent 'token'.
    for t in self.ctx.Keys() + os.listdir():
      if t.startswith(text) and all(c.isalnum() or c in '.' for c in t):
        yield t + ' '

  def __call__(self, text, i):
    try:
      if i == 0:
        self.completions = list(self.Complete(text))
      return self.completions[i] if i < len(self.completions) else None
    except BaseException as e:
      # readline swallows exceptions. I like my errors to be noisy.
      traceback.print_exc()
      exit(1)


def Repl():
  ctx = ev.Context(ev.GLOBAL)
  readline.set_completer(Completer(ctx))
  try:
    while True:
      prompt = '%s %s$ ' % (datetime.datetime.now(), os.getcwd().split('/')[-1])
      text = input(prompt) + '\n'
      d = parser.Parse(text)
      result = ev.Eval(ctx, d)
  except EOFError:
    print()


if __name__ == '__main__':
  Repl()
