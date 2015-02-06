import sys
from .translate import translate

if __name__ == '__main__':
	try:
		sys.stdout.write(translate(sys.stdin.read()))
	except SyntaxError as e:
		sys.stderr.write(str(e))
		exit(1)
