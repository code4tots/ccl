class Ast(object):

	@property
	def swift(self):
		return '\npushvalue(ctx, %s)' % self.swiftvalue

class Token(Ast, object):
	def __new__(cls, start, end, value):
		self = super(Token, cls).__new__(cls, value)
		self.start = start
		self.end = end
		return self

	@property
	def swiftvalue(self):
		return repr(self)

class Int(Token, int):
	pass

class Float(Token, float):
	pass

class Id(Token, str):
	@property
	def swift(self):
		return '\nsummonid(ctx, "%s")' % self

class QuoteFunc(Id):
	@property
	def swiftvalue(self):
		return 'ctx["%s"]' % self

class Assign(Id):
	@property
	def swift(self):
		return '\nctx["%s"] = ctx.pop()' % self

class Str(Token, str):
	@property
	def swiftvalue(self):
		return '"%s"' % ''.join('\\u{%x}' % ord(c) for c in self)

class Block(Ast, tuple):
	def __new__(cls, start, end, items):
		self = super(Block, cls).__new__(cls, items)
		self.start = start
		self.end = end
		return self

	@property
	def swiftvalue(self):
		return 'Verb {(ctx: Context) in' + ''.join(x.swift.replace('\n', '\n\t') for x in self) + '\n}'

class Top(Block):
	@property
	def swift(self):
		return ''.join((
			'\nfunc runccl() {',
			(super(Top, self).swift + '\npopandrun(ctx)').replace('\n', '\n\t'),
			'\n}'))

class List(Block):
	@property
	def swift(self):
		return ''.join((
			'\npushstack(ctx)',
			''.join(x.swift for x in self),
			'\npopstack(ctx)'))

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
					if x.startswith(('.', '=')):
						d[1] = {
							'.': QuoteFunc,
							'=': Assign,
						}[x[0]]
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
	return Top(start_stack.pop(), len(s.rstrip()), stack.pop())

d = parse('''

# (x y z) print
# ( false ) ( 'a' ) ( 'b' ) if print
# ( true ) ( 1 ) ( 2 ) if print
# ( 0 ) ('x') ('y') if print
# ( "" ) ( 'left' ) ( 'right' ) if print

"outside" =x

"x is: " print
x print

(
	"inside" =x
	x print
) =f

f

# """Hello world!
# again""" print

''')

with open('/Users/math4tots/Documents/XcodeProjects/An App A Day/Scan Books/Scan Books/cclcode.swift', 'w') as f:
	f.write(d.swift)
