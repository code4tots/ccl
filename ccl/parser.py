import re, collections

# utils

class Eq(object):
	def __eq__(self, other):
		return type(self) == type(other) and super(Eq, self).__eq__(other)

def nt(s): return collections.namedtuple('X', s)

# abstract syntax tree nodes.

class Chain(Eq, nt('lhs rhs')):
	pass

class FunctionCall(Eq, nt('f args')):
	pass

class Name(Eq, str):
	pass

class StringLiteral(Eq, str):
	pass

class NumberLiteral(Eq, str):
	pass

class FunctionLiteral(Eq, nt('args body')):
	pass

class DictLiteral(Eq, tuple):
	pass

class ListLiteral(Eq, tuple):
	pass

class Parser(object):
	NUMBER_REGEX = re.compile(r'(?:\+|\-)?(?:\d+\.\d*|\.?\d+)')
	NAME_REGEX = re.compile(r'\w+')

	def __init__(self, text):
		self.s = text
		self.a = self.b = 0
		self.token = None

		self.location_stack = []

		self.next()

	# location stack

	def push_location(self):
		self.location_stack.append((self.a, self.b))

	def pop_location(self):
		self.a, self.b = self.location_stack.pop()

	# location message

	@property
	def row(self):
		return 1 + self.s.count('\n', self.a, self.b)

	@property
	def column(self):
		return self.a - self.s.rfind('\n', 0, self.a)

	@property
	def line(self):
		a = self.s.rfind('\n', 0, self.a) + 1
		b = self.s.find('\n', self.a)
		b = len(self.s) if b == -1 else b
		return self.s[a:b]

	@property
	def location_message(self):
		return 'on line %s\n%s\n%s' % (
				self.row, self.line, ' ' * (self.column-1) + '*')

	# lexical analysis

	@property
	def c(self):
		return self.s[self.b] if self.b < len(self.s) else ''

	def __iter__(self):
		return self

	def __next__(self):
		return self.next()

	def next(self):
		if self.done:
			raise StopIteration()

		last_token = self.token

		while self.c and self.c.isspace() or self.c == '#':
			if self.c == '#':
				while self.c and self.c != '\n':
					self.b += 1
			else:
				self.b += 1

		self.a = self.b

		if self.c in ('"', "'"):
			q = self.c
			self.b += 1

			while self.c and self.c != q:
				self.b += 2 if self.c == '\\' else 1

			if self.c != q:
				raise SyntaxError('Matching quote missing ' + self.location_message)

			self.b += 1

		else:
			while self.c and not self.c.isspace():
				self.b += 1

		self.token = self.s[self.a:self.b]

		return last_token

	def consume(self, token):
		if self.token == token:
			return self.next()

	@property
	def done(self):
		return self.token == ''

	# Parse dat LL(1) grammar.

	def maybe_parse_expression(self):
		if self.consume('('):
			f = self.parse_expression()
			args = []
			while not self.consume(')'):
				args.append(self.parse_expression())
			return FunctionCall(f, tuple(args))
		elif self.consume('['):
			exprs = []
			while not self.consume(']'):
				exprs.append(self.parse_expression())
			return ListLiteral(tuple(exprs))
		elif self.consume('{'):
			exprs = []
			while not self.consume('}'):
				exprs.append((self.parse_expression(),self.parse_expression()))
			return DictLiteral(tuple(exprs))
		elif self.consume('.'):
			args = []
			while not self.consume('{'):
				if not self.NAME_REGEX.match(self.token):
					raise SyntaxError('Invalid name %s %s' % (
							self.token, self.location_message))
				args.append(self.next())
			body = self.parse_expressions()
			if not self.consume('}'):
				raise SyntaxError('Missing "}" ' + self.location_message)
			return FunctionLiteral(tuple(args), body)
		elif self.token.startswith(('"',"'")):
			return StringLiteral(self.next())
		elif self.NUMBER_REGEX.match(self.token):
			return NumberLiteral(self.next())
		elif self.NAME_REGEX.match(self.token):
			return Name(self.next())

	def parse_expression(self):
		ast = self.maybe_parse_expression()
		if ast is None:
			raise SyntaxError('Invalid expression ' + self.location_message)
		return ast

	def parse_expressions(self):
		lhs = self.maybe_parse_expression()
		if lhs is None:
			return NumberLiteral('0')
		rhs = self.maybe_parse_expression()
		while rhs is not None:
			lhs = Chain(lhs, rhs)
			rhs = self.maybe_parse_expression()
		return lhs

	def parse_all(self):
		expressions = self.parse_expressions()
		if not self.done:
			raise SyntaxError('Invalid expression ' + self.location_message)
		return expressions

assert list(Parser('a b c')) == ['a', 'b', 'c']
assert list(Parser('"hi there"')) == ['"hi there"']
assert list(Parser(': #')) == [':']
assert list(Parser(':#')) == [':#']
assert list(Parser("' # '")) == ["' # '"]

ts = Parser('abc xyz')
ts.push_location()
ts.next()
assert ts.location_message == 'on line 1\nabc xyz\n    *'

ts.pop_location()
assert ts.location_message == 'on line 1\nabc xyz\n*'

assert Parser('').parse_all() == NumberLiteral('0')
assert Parser('hi').parse_all() == Name('hi')
assert Parser('''
( . x { 2 x } 'hi' [ 4 ] { 1 2 } )
''').parse_all() == FunctionCall(
		FunctionLiteral(('x',), Chain(NumberLiteral('2'), Name('x'))),
		(
				StringLiteral("'hi'"),
				ListLiteral((NumberLiteral('4'),)),
				DictLiteral((
						(NumberLiteral('1'), NumberLiteral('2')),
				))
		)
)
