class Context(object):
	def __init__(self, parent):
		self.table = dict()
		self.parent = parent

	def __contains__(self, key):
		return key in self.table or key in self.parent

	def __getitem__(self, key):
		return self.table[key] if key in self.table else self.parent[key]

	def __setitem__(self, key, value):
		if key in self.table:
			self.table[key] = value
		else:
			self.parent[key] = value

	def declare(self, key, value=None):
		self.table[key] = value

class Ast(object):

	def evl(self, ctx):
		raise NotImplemented('%s does not implemented evaluation' % type(self))

	@property
	def swift(self):
		return '\npushvalue(%s)' % self.swiftvalue

class Token(Ast, object):
	def __new__(cls, start, end, value):
		self = super(Token, cls).__new__(cls, value)
		self.start = start
		self.end = end
		return self

	def evl(self, ctx):
		return self

	@property
	def swiftvalue(self):
		return repr(self)

class Int(Token, int):
	pass

class Float(Token, float):
	pass

class Id(Token, str):
	def evl(self, ctx):
		return ctx[str(self)]

	@property
	def swift(self):
		return '\nsummonid("%s")' % self

class QuoteFunc(Id):
	@property
	def swiftvalue(self):
		return 'ctx[%s]' % self

class Str(Token, str):
	@property
	def swiftvalue(self):
		return repr(self)

class Block(Ast, tuple):
	def __new__(cls, start, end, items):
		self = super(Block, cls).__new__(cls, items)
		self.start = start
		self.end = end
		return self

	def evl(self, ctx):
		return self

	def exc(self, ctx):
		for item in self:
			value = item.evl(ctx)
			if not isinstance(value, Func) or isinstance(item, QuoteFunc):
				ctx['__stack__'].append(value)
			else:
				value(ctx)

	@property
	def swiftvalue(self):
		return '{' + ''.join(x.swift.replace('\n', '\n\t') for x in self) + '\n}'

class List(Block):
	def evl(self, ctx):
		return [item.evl(ctx) for item in self]

class Func(object):
	def __init__(self, cb):
		self.callback = cb

	def __call__(self, ctx):
		return self.callback(ctx)

EOF = 'EOF'

def parse(s):
	# Really ugly code from a design perspective.
	# But just wanna quick hack.

	d = [ # Workaround Python 2 scoping limitations.
		0,    # 0 -> current location
		None, # 1 -> curret token type
		None, # 2 -> current token value
		None, # 3 -> current token start location
	]

	def tt(): # token type
		return d[1]

	def tv(): # token value
		return d[2]

	def ts(): # token start
		return d[3]

	def i(): # current location
		return d[0]

	def inc(di=1):
		d[0] += di

	def ch(di=1):
		return s[i():i()+di]

	def startswith(ss):
		return s.startswith(ss, i())

	def skip_spaces():
		while ch().isspace() or ch() == '#':
			if ch() == '#':
				while ch() and ch() != '\n':
					inc()
			else:
				inc()

	def next_token():
		skip_spaces()

		d[3] = d[0]

		if not ch():
			d[1] = d[2] = EOF

		elif ch() in '[]()':
			d[1] = d[2] = ch()
			inc()

		elif ch() == ';':
			d[1] = d[2] = Invoke
			inc()

		elif startswith(('r"', "r'", '"', "'")):

			d[1] = Str

			if ch() == 'r':
				inc()

			if startswith(('"""', "'''")):
				q = ch(3)
				inc(3)
			else:
				q = ch()
				inc()

			while not startswith(q):
				inc()

			inc(len(q))

			d[2] = eval(s[ts():i()])

		else:
			while ch() and ch() not in "'" '"[]();' and not ch().isspace():
				inc()

			x = s[d[3]:i()]

			assert x, s[i():]

			try:
				d[1] = Int
				d[2] = int(x)
			except ValueError:
				try:
					d[1] = Float
					d[2] = float(x)
				except ValueError:
					if x.startswith('.'):
						d[1] = QuoteFunc
						d[2] = x[1:]
					else:
						d[1] = Id
						d[2] = x

	stack = [[]]

	skip_spaces()

	start_stack = [i()]

	next_token()
	while tt() != EOF:
		if tt() in ('[', '('):
			stack.append([])
			start_stack.append(ts())
		elif tt() in (']', ')'):
			stack[-2].append((List if tt() == ']' else Block)(start_stack.pop(), i(), stack.pop()))
		else:
			stack[-1].append(tt()(ts(), i(), tv()))
		next_token()

	assert len(stack) == 1, stack

	return Block(start_stack.pop(), len(s.rstrip()), stack.pop())

CCL_GLOBALS = {'true': True, 'false': False}

def GLOBAL_FUNC(name):
	def GLOBAL_FUNC_inside(func):
		CCL_GLOBALS[name] = Func(func)
	return GLOBAL_FUNC_inside

@GLOBAL_FUNC('if')
def _(ctx):
	stack = ctx['__stack__']
	cond, a, b = stack[-3:]
	del stack[-3:]

	cond.exc(ctx)
	if stack.pop():
		a.exc(ctx)
	else:
		b.exc(ctx)

@GLOBAL_FUNC('while')
def _(ctx):
	stack = ctx['__stack__']
	cond, body = stack[-2:]
	del stack[-2:]

	while True:
		cond.exc(ctx)
		if not stack.pop():
			break

		body.exc(ctx)

@GLOBAL_FUNC('print')
def _(ctx):
	print(ctx['__stack__'].pop())

d = parse('''

# (x y z) print
( false ) ( 'a' ) ( 'b' ) if print

''')

ctx = Context(CCL_GLOBALS)
ctx['__stack__'] = []
d.exc(ctx)

print d.swift