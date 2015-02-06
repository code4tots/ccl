"""corelib.py is the most fundamental module.

The parser depends on this module.

corelib.py and langlib.py are very similar in style,
but langlib.py depends on corelib.py.
"""
import collections

class MemoedType(type):
	def __init__(cls, name, bases, dict_):
		cls.instances.append(cls)

class Ast(object):
	@staticmethod
	def parse(parser):
		pass

	def __eq__(self, other):
		return type(self) == type(other) and super(Ast, self).__eq__(other)

	def __ne__(self, other):
		return not (self == other)

Atom = MemoedType('Atom', (Ast,), {'instances': []})
Type = MemoedType('Type', (Ast,), {
		'instances': [],
		'__str__': lambda self: self.declare('').strip(),
		'supers': (),
})

def NamedTuple(s):
	class NamedTuple(collections.namedtuple('NamedTuple', s)):
		def __eq__(self, other):
			return type(other) == type(self) and tuple.__eq__(self, other)
	return NamedTuple

def AtomTuple(s):
	class AtomTuple(Atom, NamedTuple(s)):
		def __new__(cls, *args, **kwargs):
			self = super(AtomTuple, cls).__new__(cls, *args, **kwargs)
			if hasattr(cls, 'same_type_as'):
				self.type = getattr(self, cls.same_type_as).type
			return self
	return AtomTuple

def TypeTuple(s):
	class TypeTuple(Type, NamedTuple(s)):
		pass
	return TypeTuple

class SimpleType(Type):
	@classmethod
	def parse(cls, s):
		if s.consume(cls.name):
			return cls()

	def declare(self, inside):
		return '%s %s' % (self.name, inside)

	def __eq__(self, other):
		return type(self) == type(other)

class Number(SimpleType):
	name = 'number'

class String(SimpleType):
	name = 'string'

class NoOp(Atom):
	type = Number()

	def __str__(self):
		return '0'

	def __eq__(self, other):
		return type(self) == type(other)

class Chain(AtomTuple('lhs rhs')):
	same_type_as = 'rhs'

	def __str__(self):
		return '([](%s,%s){return rhs;}(%s,%s))' % (
				self.lhs.type.declare('lhs'),
				self.rhs.type.declare('rhs'),
				self.lhs, self.rhs)

class NumberLiteral(Atom, str):
	type = Number()

	@staticmethod
	def parse(s):
		if s.token and all(c.isdigit() or c in '+-.' for c in s.token):
			return NumberLiteral(s.next())

class StringLiteral(Atom, str):
	type = String()

	@staticmethod
	def parse(s):
		if s.token.startswith(':'):
			return StringLiteral(s.next()[1:])

	def __str__(self):
		return '"' + self + '"'

class Name(AtomTuple('type name')):

	@staticmethod
	def parse(s):
		if s.valid_name(s.token):
			return Name(s[s.token], s.next())

	def __str__(self):
		return self.name

class Bind(NamedTuple('parser name type')):
	def __enter__(self):
		self.parser.name_stack.append((self.name, self.type))

	def __exit__(self, *_):
		self.parser.name_stack.pop()

class Let(AtomTuple('name value block')):
	same_type_as = 'block'

	@staticmethod
	def parse(s):
		if s.consume('.let'):
			name = s.parse_name_token()
			value = s.parse_atom()
			with Bind(s, name, value.type):
				block = s.parse_many_atoms()
			return Let(name, value, block)

	def __str__(self):
		return '([](%s){return %s;}(%s))' % (
				self.value.type.declare(self.name), self.block, self.value)
