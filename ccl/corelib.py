class MemoedType(type):
	def __init__(cls, name, bases, dict_):
		cls.instances.append(cls)

class Ast(object):
	def parse(self, parser):
		pass

	def __eq__(self, other):
		return type(self) == type(other) and super(Ast, self).__eq__(other)

Atom = MemoedType('Atom', (Ast,), {'instances': []})
Type = MemoedType('Type', (Ast,), {'instances': []})

def NamedTuple(s):
	class NamedTuple(collections.namedtuple('NamedTuple', s)):
		def __eq__(self, other):
			return type(other) == type(self) and tuple.__eq__(self, other)

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
	def declare(self, inside):
		return '%s %s' % (self.name, inside)

	def __eq__(self, other):
		return type(self) == type(other)

class Void(SimpleType):
	name = 'void'

class Number(SimpleType):
	name = 'number'

class String(SimpleType):
	name = 'string'

class NoOp(Atom):
	type = Void()

	def __str__(self):
		return ''

	def __eq__(self, other):
		return type(self) == type(other)

class Chain(AtomTuple('lhs rhs')):
	same_type_as = 'rhs'

	def __str__(self):
		return '([](%s,%s){return rhs;})(%s,%s)' % (
				self.lhs.type.declare('lhs'),
				self.rhs.type.declare('rhs'),
				self.lhs, self.rhs)

class NumberLiteral(Atom, str):
	type = Number()

	def parse(self, s):
		if s.token and all(c.isdigit() or c in '+-.' for c in s.token):
			return NumberLiteral(s.next())

class StringLiteral(Atom, str):
	type = String()

	def parse(self, s):
		if s.token.startswith(':'):
			return StringLiteral(s.next()[1:])

	def __str__(self):
		return '"' + self + '"'
