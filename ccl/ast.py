import collections, re
from .lexer import TokenStream

def parse(string):
	return Chain.parse(TokenStream(string))

def nt(s): return collections.namedtuple('X', s)

class Singleton(object):
	def __new__(cls):
		if cls._singleton is None:
			cls._singleton = super(Singleton, cls).__new__(cls)
		return cls._singleton

	def __eq__(self, other):
		return type(self) == type(other)

class Ast(object):
	registered_parsers = []

	same_type_as = None

	def __new__(cls, *args, **kwargs):
		self = super(Ast, cls).__new__(cls, *args, **kwargs)
		if cls.same_type_as is not None:
			self.type = getattr(self, cls.same_type_as).type
		return self

	@classmethod
	def register_parser(cls, parser):
		cls.registered_parsers.append(parser)
		return parser

	@classmethod
	def parse_any(cls, s):
		for parser in cls.registered_parsers:
			ast = parser.parse(s)
			if ast is not None:
				return ast

	@staticmethod
	def expect_type(ast, expected_type, s):
		if ast is None:
			raise SyntaxError('Expected %s but found invalid expression %s' % (
					expected_type, s.location_message))

		if not ast.is_a(expected_type):
			raise SyntaxError('Expected %s but got %s %s' % (
					expected_type, ast.type, s.location_message))

	@classmethod
	def parse(cls, expected_type, s):
		ast = cls.parse_any(s)
		cls.expect_type(ast, expected_type, s)
		return ast

	def __eq__(self, other):
		return type(self) == type(other) and super(Ast, self).__eq__(other)

	def is_a(self, type_):
		return self.type.is_subclass_of(type_)

class Type(Ast):
	def is_subclass_of(self, type_):
		return self == type_ or any(
				base.is_subclass_of(type_) for base in self.bases)

class ExpressionType(Type, Singleton):
	_singleton = None

class NumberType(Type, Singleton):
	bases = (ExpressionType(),)
	_singleton = None

class StringType(Type, Singleton):
	bases = (ExpressionType(),)
	_singleton = None

class NoOp(Ast, Singleton):
	_singleton = None
	type = NumberType()

class Chain(Ast, nt('lhs rhs')):
	same_type_as = 'rhs'

	@classmethod
	def parse(cls, s):
		lhs = Ast.parse_any(s)
		if lhs is None:
			return NoOp()
		Ast.expect_type(lhs, ExpressionType(), s)

		rhs = cls.parse(s)
		if rhs == NoOp():
			return lhs
		Ast.expect_type(rhs, ExpressionType(), s)

		return Chain(lhs, rhs)

@Ast.register_parser
class NumberLiteral(Ast, str):
	type = NumberType()

	REGEX = re.compile(r'(?:\+|\-)?(?:\d+\.\d*|\.?\d+)')

	@classmethod
	def parse(cls, s):
		if cls.REGEX.match(s.token):
			return NumberLiteral(s.next())

@Ast.register_parser
class StringLiteral(Ast, str):
	type = StringType()

	@staticmethod
	def parse(s):
		if s.token.startswith(':'):
			return StringLiteral(s.next()[1:])

### tests

assert parse('') == NoOp()
assert parse('5') == NumberLiteral('5')
assert parse('5.') == NumberLiteral('5.')
assert parse('.5') == NumberLiteral('.5')
assert parse(':x') == StringLiteral('x')
