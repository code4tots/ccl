import collections, re, sys

HEADER = '''
#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
using namespace std;
typedef long double number;
'''

def nt(s):
	"""Wrapper around namedtuple."""
	class X(collections.namedtuple('X', s)):
		def __eq__(self, other):
			return isinstance(other, type(self)) and tuple.__eq__(self, other)
	return X

def ntt(s):
	"""nt for types."""
	return nt(s)

def nte(s):
	"""nt for expressions."""
	class X(nt(s)):
		def __new__(cls, *args, **kwargs):
			self = super(X, cls).__new__(cls, *args, **kwargs)
			if hasattr(cls, 'same_type_as'):
				self.type = getattr(self, cls.same_type_as).type
			return self
	return X

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

class Bind(nt('stream name type')):
	def __enter__(self):
		self.stream.stack.append((self.name, self.type))

	def __exit__(self, *_):
		self.stream.stack.pop()

class Stream(object):
	def __init__(self, string):
		self.gen = iter(re.sub(r'#.*?(\n|\Z)', '\n', string).split() + [''])
		self.token = next(self.gen)
		self.stack = [
			('cin', Istream()),
			('cout', Ostream())]

	def next(self):
		last_token = self.token
		self.token = next(self.gen)
		return last_token

	def consume(self, token):
		if self.token == token:
			return self.next()

	def __getitem__(self, name):
		for name_, type_ in reversed(self.stack):
			if name == name_:
				return type_
		raise ValueError('No variable named "%s" has been declared' % (name,))

	def parse(self):
		lhs = self.parse_atom()
		if lhs is not None:
			rhs = self.parse()
			return lhs if rhs is None else Chain(lhs, rhs)

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

## types

class SimpleType(ntt('')):
	@classmethod
	def parse(cls, s):
		if s.consume(cls.name):
			return cls()

	def declare(self, inside):
		return self.name + ' ' + inside

	def __eq__(self, other):
		return isinstance(other, type(self))

@register_type
class StringType(SimpleType):
	name = 'string'

@register_type
class NumberType(SimpleType):
	name = 'number'

@register_type
class Istream(SimpleType):
	name = 'istream'

@register_type
class Ostream(SimpleType):
	name = 'ostream'

class Reference(ntt('type')):
	def __new__(cls, type_):
		return (type_ if isinstance(type_, Reference) else
				super(Reference, cls).__new__(cls, type_))

	def declare(self, inside):
		return self.type.declare('(&%s)' % (inside,))

## expressions

class Chain(nte('lhs rhs')):
	same_type_as = 'rhs'

	def __str__(self):
		return '([](%s,%s){return rhs;})(%s,%s)' % (
				self.lhs.type.declare('lhs'),
				self.rhs.type.declare('rhs'),
				self.lhs, self.rhs)

@register_atom
class NumberLiteral(str):
	type = NumberType()

	@staticmethod
	def parse(s):
		if s.token and all(c.isdigit() or c in '+-.' for c in s.token):
			return NumberLiteral(s.token)

@register_atom
class StringLiteral(str):
	type = StringType()

	@staticmethod
	def parse(s):
		if s.token and s.token.startswith(':'):
			return StringLiteral(s.next()[1:])

	def __str__(self):
		return '"' + self + '"'

@register_atom
class Name(nte('type name')):
	@staticmethod
	def parse(s):
		if s.token and all(c.isalnum() or c in '_' for c in s.token):
			return Name(s[s.token], s.next())

	def __str__(self):
		return self.name

@register_atom
class Let(nte('name value block')):
	same_type_as = 'block'

	@staticmethod
	def parse(s):
		if s.consume('.let'):
			name = s.next()
			value = s.parse_atom(True)
			with Bind(s, name, value.type):
				block = s.parse()
			return Let(name, value, block)

	def __str__(self):
		return '([&](%s){return %s;})(%s)' % (
				self.value.type.declare(self.name),
				self.block, self.value)

@register_atom
class Block(nte('expression')):
	same_type_as = 'expression'

	@staticmethod
	def parse(s):
		if s.consume('{'):
			expression = s.parse()
			assert s.consume('}')
			return Block(expression)

	def __str__(self):
		return str(self.expression)

@register_atom
class Space(nte('')):
	type = StringType()

	@staticmethod
	def parse(s):
		if s.consume(r'\s'):
			return Space()

	def __str__(self):
		return '" "'

@register_atom
class Newline(nte('')):
	type = StringType()

	@staticmethod
	def parse(s):
		if s.consume(r'\n'):
			return Newline()

	def __str__(self):
		return r'"\n"'

@register_atom
class StringStream(nte('args')):
	type = StringType()

	@staticmethod
	def parse(s):
		if s.consume('str('):
			args = []
			while not s.consume(')'):
				args.append(s.parse_atom(True))
			return StringStream(tuple(args))

	def __str__(self):
		return '([](%s){ostringstream ss;%s;return ss.str();})(%s)' % (
				','.join(arg.type.declare('x'+str(i))
						for i, arg in enumerate(self.args)),
				';'.join('ss<<x'+str(i) for i in range(len(self.args))),
				','.join(map(str, self.args)))

@register_atom
class Write(nte('stream value')):
	same_type_as = 'value'

	@staticmethod
	def parse(s):
		if s.consume('.write'):
			return Write(s.parse_atom(True), s.parse_atom(True))

	def __str__(self):
		return '([](%s,%s){fout<<x;return x;})(%s,%s)' % (
				Reference(self.stream.type).declare('fout'),
				self.value.type.declare('x'),
				self.stream, self.value)

@register_atom
class Read(nte('type stream')):
	@staticmethod
	def parse(s):
		if s.consume('.read'):
			return Read(s.parse_type(True), s.parse_atom(True))

	def __str__(self):
		return '([](%s){%s;fin>>x;return x;})(%s)' % (
				Reference(self.stream.type).declare('fin'),
				self.type.declare('x'), self.stream)

if __name__ == '__main__':
	sys.stdout.write(translate(sys.stdin.read()))
