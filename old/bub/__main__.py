import sys

from . import Run

if len(sys.argv) == 1:
  Run(sys.stdin.read())
else:
  with open(sys.argv[1]) as f:
    content = f.read()
  Run(content)
