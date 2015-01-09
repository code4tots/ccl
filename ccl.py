#!/usr/bin/python

import code, os, sys, readline, rlcompleter

PATH = os.environ['PATH'].split(os.pathsep)

class ShellService(object):

  def __getitem__(self, attribute):
    for path in PATH:
      os.listdir(path)
    raise AttributeError(attribute)

X = ShellService()



def run_file(file_path):
  execfile(file_path, globals())

def repl():
  readline.parse_and_bind('bind ^I rl_complete' if sys.platform == 'darwin' else 'tab: complete')
  console = code.InteractiveConsole(locals=globals())
  while console.interact('-- ccl shell --'): pass

if __name__ == '__main__':
  repl()
