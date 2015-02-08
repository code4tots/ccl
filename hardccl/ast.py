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

	@classmethod
	def parse_expression(cls, s):
		ast = cls.parse_any(s)
		if ast is not None and not isinstance(ast, Expression):
			raise SyntaxError('Expected expression but got %s %s' % (
					'invalid expression' if ast is None else ast.type,
					s.location_message))
		return ast

	@staticmethod
	def expect_type(ast, expected_type, s):
		if ast is None:
			raise SyntaxError('Expected %s but found invalid expression %s' % (
					expected_type, s.location_message))

		if ast.type != expected_type:
			raise SyntaxError('Expected %s but got %s %s' % (
					expected_type, ast.type, s.location_message))

	@classmethod
	def parse_expression_of_type(cls, expected_type, s):
		ast = cls.parse_any(s)
		cls.expect_type(ast, expected_type, s)
		return ast

	def __eq__(self, other):
		return type(self) == type(other) and super(Ast, self).__eq__(other)

class Type(Ast):
	pass

class VoidType(Type, Singleton):
	_singleton = None

class NumberType(Type, Singleton):
	_singleton = None

class StringType(Type, Singleton):
	_singleton = None

class Expression(Ast):
	pass

class NoOp(Expression, Singleton):
	_singleton = None
	type = VoidType()

class Chain(Expression, nt('lhs rhs')):
	same_type_as = 'rhs'

	@classmethod
	def parse(cls, s):
		lhs = Ast.parse_expression(s)
		if lhs is None:
			return NoOp()

		rhs = cls.parse(s)
		if rhs == NoOp():
			return lhs

		return Chain(lhs, rhs)

@Ast.register_parser
class NumberLiteral(Expression, str):
	type = NumberType()

	REGEX = re.compile(r'(?:\+|\-)?(?:\d+\.\d*|\.?\d+)')

	@classmethod
	def parse(cls, s):
		if cls.REGEX.match(s.token):
			return NumberLiteral(s.next())

@Ast.register_parser
class StringLiteral(Expression, str):
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
assert parse('5.5') == NumberLiteral('5.5')
assert parse(':') == StringLiteral('')
assert parse(':x') == StringLiteral('x')
