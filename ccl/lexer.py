import collections

class Bind(collections.namedtuple('Bind', 'stream name value_type')):
	def __enter__(self):
		self.stream.name_type_stack.append((self.name, self.value_type))

	def __exit__(self, *_):
		self.stream.name_type_stack.pop()

class TokenStream(object):
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

	def bind(self, name, value_type):
		return Bind(self, name, value_type)

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

### tests

assert list(TokenStream('a b c')) == ['a', 'b', 'c']
assert list(TokenStream(': #')) == [':']
assert list(TokenStream(':#')) == [':#']

ts = TokenStream('abc xyz')
with ts.bind('a', 'b'):
	with ts.bind('a', 'c'):
		assert ts['a'] == 'c'
	assert ts['a'] == 'b'

ts.push_location()
ts.next()
assert ts.location_message == 'on line 1\nabc xyz\n    *'

ts.pop_location()
assert ts.location_message == 'on line 1\nabc xyz\n*'
