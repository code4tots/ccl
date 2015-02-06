from .ast import Ast, NoOp, Chain

class Parser(object):
	def __init__(self, text):
		self.s = text
		self.a = self.b = 0
		self.token = None

		self.location_stack = []

		self.name_type_stack = []

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
		b = self.s.find('\n', self.b)
		b = len(self.s) if b == -1 else b
		return self.s[a:b]

	@property
	def location_message(self):
		return 'on line %s\n%s\n%s' % (
				self.row, self.line, ' ' * (self.column-1) + '*')

	# name type stack

	def __getitem__(self, key):
		for name, type_ in reversed(self.name_type_stack):
			if name == key:
				return type_
		raise SyntaxError('%s not defined in scope %s' % (
				key, self.location_message))

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

	# parsing.

	def parse_one(self):
		for ast_cls in Ast.ast_clss:
			ast = ast_cls.parse(self)
			if ast is not None:
				return ast

	def __call__(self, type_):
		self.push_location()
		ast = self.parse_one()
		if not ast or not ast.is_a(type_):
			self.pop_location()
			raise SyntaxError('Expected %s but got %s %s' % (
					type_, 'eof' if ast is None else ast.type,
					self.location_message))
		return ast

	def parse_chain(self, to_completion=False):
		ast = NoOp()
		try:
			while not self.done:
				ast = Chain(ast, self(ExpressionType()))
		except SyntaxError:
			if to_completion:
				raise
		return ast

assert list(Parser('a b c ! @ #')) == ['a', 'b', 'c', '!', '@']
assert list(Parser('# comment')) == []
assert list(Parser(':#')) == [':#']

from .ast import *

assert Parser('').parse_chain() == NoOp()
assert Parser(':x').parse_chain() == Chain(NoOp(), StringLiteral('x'))
assert Parser('.list').parse_chain(to_completion=True)
