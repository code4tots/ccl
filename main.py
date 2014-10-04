from ccl import run, repl
from sys import argv
# repl()

with open(argv[1]) as f:
    run(f.read())
