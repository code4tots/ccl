from collections import namedtuple

class AstMetaclass(type):
	def __new__(mcs, name, bases, dict_):
		cls = super(AstMetaclass, mcs).__new__(mcs, name, bases, dict_)
		cls.ast_clss.append(cls)
		return cls

BaseAst = AstMetaclass('BaseAst', (), {
		'ast_clss': [],
		'parse': staticmethod(lambda s: None),
})

class Ast(BaseAst):
	def __new__(cls, *args, **kwargs):
		self = super(Ast, cls).__new__(cls, *args, **kwargs)
		if hasattr(self, 'same_type_as'):
			self.type = getattr(self, self.same_type_as).type
		return self

	def __eq__(self, other):
		return type(self) == type(other) and super(Ast, self).__eq__(other)

	def is_a(self, type_):
		return type_ in self.type.supers	

class Type(Ast):
	_supers = None

	@property
	def supers(self):
		if self._supers is None:
			self._supers = tuple(set([self] + list(
					sup for base in self.bases for sup in base.supers)))
		return self._supers

class PrimitiveType(Type):
	name = ''

	@classmethod
	def parse(cls, s):
		if s.consume('.' + cls.name):
			return cls()

	def __hash__(self):
		return hash(type(self))

	def __eq__(self, other):
		return type(self) == type(other)

	def __str__(self):
		return self.name

class TypeType(PrimitiveType):
	bases = ()
	name = 'type'

# It's contentious whether TypeType should be a Type
Type.type = TypeType()

class ExpressionType(PrimitiveType):
	bases = ()
	name = 'expression'

class NumberType(PrimitiveType):
	bases = (ExpressionType(),)
	name = 'number'

class StringType(PrimitiveType):
	bases = (ExpressionType(),)
	name = 'string'

def TypeTuple(s):
	class TypeTuple(Type, namedtuple('TypeTuple', s)):
		pass
	return TypeTuple

class ListType(TypeTuple('value_type')):
	type = TypeType

	@staticmethod
	def parse(s):
		if s.consume('.list'):
			return ListType(s(TypeType()))

class DictType(TypeTuple('key_type value_type')):
	type = TypeType

	@staticmethod
	def parse(s):
		if s.consume('.dict'):
			return DictType(s(TypeType()), s(TypeType()))

class Expression(Ast):
	pass

def ExpressionTuple(s):
	class ExpressionTuple(Expression, namedtuple('ExpressionTuple', s)):
		pass
	return ExpressionTuple

class Chain(ExpressionTuple('lhs rhs')):
	same_type_as = 'rhs'

class NoOp(Expression):
	type = NumberType()

	def __eq__(self, other):
		return type(self) == type(other)

class NumberLiteral(Expression, str):
	type = NumberType()

	@staticmethod
	def parse(s):
		if s.token and all(c.isdigit() or c in '+-.' for c in s.token):
			return NumberLiteral(s.next())

class StringLiteral(Expression, str):
	type = StringType()

	@staticmethod
	def parse(s):
		if s.token.startswith(':'):
			return StringLiteral(s.next()[1:])

class Name(ExpressionTuple('type name')):
	@staticmethod
	def parse(s):
		if s.token and all(c.isalnum() or c in '_' for c in s.token):
			return Name(s[s.token], s.next())

assert Chain(StringLiteral('x'), NoOp()).type == NoOp().type == NumberType()
assert NoOp() == NoOp()
assert Chain(NoOp(), NoOp()) == Chain(NoOp(), NoOp())
