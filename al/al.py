import collections, sys
def nt(s): return collections.namedtuple('x', s)

class Stream(object):
	def __init__(self, string):
		self.gen = iter(string.split() + [None])
		self.token = next(self.gen)

	def next(self):
		old = self.token
		self.token = next(self.gen)
		return old

types = []
asts = []

def ast(a):
	asts.append(a)
	return a

def parse(stream):
	for a in asts:
		x = a.parse(stream)
		if x is not None:
			return x
	raise ValueError('no parse')

def translate(string):
	with open('header.hpp') as f:
		s = f.read()
	stream = Stream(string)
	s += 'int main(){'
	while stream.token is not None:
		s += str(parse(stream)) + ';'
	s += '}'
	return s

@ast
class Let(nt('name value expr')):
	@classmethod
	def parse(cls, stream):
		if stream.token.endswith('='):
			name = stream.next()[:-1]
			value = parse(stream)
			expr = parse(stream)
			return Let(name, value, expr)

	@property
	def type(self):
		try:
			types.append((self.name, self.value.type))
			return self.expr.type
		finally:
			types.pop()

	def __str__(self):
		return '([&](%s %s){return %s;})(%s)' % (self.value.type, self.name, self.expr, self.value)

@ast
class Print(nt('expr')):
	@classmethod
	def parse(cls, stream):
		if stream.token == '.':
			stream.next()
			return Print(parse(stream))

	def __str__(self):
		return '([](%s x){cout << x; return x;})(%s)' % (self.expr.type, self.expr)

@ast
class Name(str):

	@classmethod
	def parse(cls, stream):
		if all(c.isalnum() or c in '_$' for c in stream.token):
			return Name(stream.next())

	@property
	def type(self):
		for n, t in reversed(types):
			if n == self:
				return t
		raise KeyError("Name %s not found" % self)

@ast
class Str(str):

	@classmethod
	def parse(cls, stream):
		if stream.token.startswith("'"):
			return Str(stream.next()[1:])

	type = 'string'

	def __str__(self):
		return '"' + self + '"'

if __name__ == '__main__':
	sys.stdout.write(translate(sys.stdin.read()))

