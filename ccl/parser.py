import re, collections

# utils

class Eq(object):
	def __eq__(self, other):
		return type(self) == type(other) and super(Eq, self).__eq__(other)

# abstract syntax tree nodes.

class MacroCall(Eq, collections.namedtuple('MacroCall', 'f args')):
	pass

class Name(Eq, str):
	pass

class StringLiteral(Eq, str):
	pass

class NumberLiteral(Eq, str):
	pass

class ParserMetaclass(type):
	def __getitem__(cls, string):
		return cls(string).parse()

class Parser(ParserMetaclass('Parser', (object,), {})):
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

	def parse_expression(self):
		if self.consume('('):
			f = self.parse_expression()
			args = []
			while not self.consume(')'):
				args.append(self.parse_expression())
			return MacroCall(f, tuple(args))
		elif self.token.startswith(('"',"'")):
			return StringLiteral(self.next())
		elif self.NUMBER_REGEX.match(self.token):
			return NumberLiteral(self.next())
		elif self.NAME_REGEX.match(self.token):
			return Name(self.next())

		raise SyntaxError("Invalid token %s %s" % (self.token, self.location_message))

	def parse(self):
		exprs = []
		while not self.done:
			exprs.append(self.parse_expression())
		return exprs

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

assert Parser['a b c'] == [Name('a'), Name('b'), Name('c')]
assert Parser['"a"'] == [StringLiteral('"a"')]
assert Parser['5'] == [NumberLiteral('5')]
assert Parser['( a b c )'] == [MacroCall(Name('a'), (Name('b'), Name('c')))]
