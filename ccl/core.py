import collections
from .corelib import NoOp, Chain

HEADER = '''
#include <string>
using namespace std;
typedef long double number;
'''

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
		return self.string[begin:end]

	@property
	def line_number(self):
		return self.string.count('\n', 0, self.begin) + 1

	@property
	def column_number(self):
		return self.begin - self.string.rfind('\n', 0, self.begin)

	@property
	def location_message(self):
		return 'on line %s:\n%s\n%s\n' % (
				self.line_number, self.line,
				' ' * (self.column_number - 1) + '*')

	@property
	def char(self):
		return self.string[self.end:self.end+1]

	@property
	def done(self):
		return self.token == ''

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

	def parse_ast(self, base_ast_cls):
		for cls in base_ast_cls.instances:
			ast = cls.parse(self)
			if ast is not None:
				return ast

		raise SyntaxError('Expected %s %s' % (
				base_ast_cls.__name__, self.location_message))

	def parse_atom(self):
		self.parse_ast(Atom)

	def parse_type(self):
		self.parse_ast(Type)

	def parse_many_atoms(self, to_completion=False):
		expression = NoOp()
		try:
			while True:
				expression = Chain(expression, self.parse_atom())
		except SyntaxError:
			if to_completion and not self.done:
				raise
		return atoms

	def parse_all(self):
		return self.parse_many_atoms(to_completion=True)

	def translate(self):
		return '%s\nint main(int argc, char** argv){%s;}\n' % (
				HEADER, self.parse_all())
