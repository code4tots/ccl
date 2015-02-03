import re, sys

HEADER = '''
#include <iostream>
#include <fstream>
#include <string>
using namespace std;
'''

def translate(string):
	return '%s\nint main(){%s;}\n' % (HEADER, Stream(string).parse() or '')

ATOMS = []

def register_atom(cls):
	ATOMS.append(cls)
	return cls

TYPES = []

def register_type(cls):
	TYPES.append(cls)
	return cls

class Stream(object):
	def __init__(self, string):
		self.gen = iter(re.sub(r'#.*?\n', '\n', string).split() + [''])
		self.token = next(self.gen)

	def next(self):
		last_token = self.token
		self.token = next(self.gen)
		return last_token

	def consume(self, token):
		if self.token == token:
			return self.next()

	def parse(self):
		lhs = self.parse_atom()
		if lhs is not None:
			rhs = self.parse()
			return lhs if rhs is None else ChainExpression(lhs, rhs)

	def parse_generic(self, clss, require):
		for cls in clss:
			result = cls.parse(self)
			if result is not None:
				return result
		if require:
			raise SyntaxError()

	def parse_atom(self, require=False):
		return self.parse_generic(ATOMS, require)

	def parse_type(self, require=False):
		return self.parse_generic(TYPES, require)

if __name__ == '__main__':
	sys.stdout.write(translate(sys.stdin.read()))
