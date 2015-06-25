class Ast(object):

	def exc(self, ctx):
		raise NotImplemented('%s does not yet implement execution' % type(self))

class Token(Ast, object):
	def __new__(cls, start, end, value):
		self = super(Token, cls).__new__(cls, value)
		self.start = start
		self.end = end
		return self

class Int(Token, int):
	pass

class Float(Token, float):
	pass

class Id(Token, str):
	pass

class Str(Token, str):
	pass

class Block(Ast, tuple):
	def __new__(cls, start, end, items):
		self = super(Block, cls).__new__(cls, items)
		self.start = start
		self.end = end
		return self

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
		s.startswith(ss, i())

	def skip_spaces():
		while ch().isspace():
			inc()

	def next_token():
		skip_spaces()

		d[3] = d[0]

		if not ch():
			d[1] = d[2] = EOF

		elif ch() in '[];':
			d[1] = d[2] = ch()
			inc()

		elif startswith(('r"', "r'", '"', "'")):

			d[1] = Str

			if ch() == 'r':
				inc()

			if startswith('"""', "'''"):
				inc(3)
				q = ch(3)

			else:
				inc()
				q = ch()

			while not startswith(q):
				inc()

			inc(len(q))

			d[2] = eval(s[d[3]:i()])

		else:
			while ch() and ch() not in ('"', "'", '[', ']', ';') and not ch().isspace():
				inc()

			x = s[d[3]:i()]

			assert x

			try:
				d[1] = Int
				d[2] = int(x)
			except ValueError:
				try:
					d[1] = Float
					d[2] = float(x)
				except ValueError:
					d[1] = Id
					d[2] = x

	stack = [[]]

	skip_spaces()

	start_stack = [i()]

	next_token()
	while tt() != EOF:
		if tt() == '[':
			stack.append([])
			start_stack.append(ts())
		elif tt() == ']':
			stack[-2].append(Block(start_stack.pop(), i(), stack.pop()))
		else:
			stack[-1].append(tt()(ts(), i(), tv()))
		next_token()

	assert len(stack) == 1, stack

	return Block(0, len(s.rstrip()), stack.pop())

print(parse('''

a b c [ 1 2 3.5 ]

'''))
