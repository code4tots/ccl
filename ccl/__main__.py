import sys
from .core import Parser

if __name__ == '__main__':
	try:
		sys.stdout.write(Parser(sys.stdin.read()).translate())
	except SyntaxError as e:
		sys.stderr.write(str(e))
