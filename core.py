class MemoedType(type):
	def __init__(cls, name, bases, dict_):
		if 'parse' in dict_:
			cls.instances.append(cls)

Atom = MemoedType('Atom', (), {'instances': []})
Type = MemoedType('Type', (), {'instances': []})

class Parser(object):
	def __init__(self, string):
		self.string = string
		self.token = None
		self.begin = 0
		self.end = 0
		self.name_stack = []

		self.next()

	@property
	def line(self):
		begin = self.string.rfind('\n', 0, self.begin) + 1
		end = self.string.find('\n', self.end)
		end = len(self.string) if end == -1 else end

	@property
	def line_number(self):
		return self.string.count('\n', 0, self.begin) + 1

	@property
	def column_number(self):
		return self.begin - self.string.rfind('\n', 0, self.begin)

	@property
	def char(self):
		return self.string[self.end:self.end+1]

	def __iter__(self):
		return self

	def __next__(self):
		return self.next()

	def next(self):
		if self.token == '':
			raise StopIteration()

		last_token = self.token

		while self.char and self.char.isspace():
			self.end += 1

		self.start = self.end

		while self.char and not self.char.isspace():
			self.end += 1

		self.token = self.string[self.start:self.end]

		return last_token

	def parse_ast(self, base_ast_cls, require):
		for cls in base_ast_cls.instances:
			ast = cls.parse(self)
			if ast is not None:
				return ast
		if require:
			raise SyntaxError("Expected " + base_ast_cls.__name__)

	def parse_atom(self, require=True):
		self.parse_ast(Atom, require)

	def parse_type(self, require=True):
		self.parse_ast(Type, require)
