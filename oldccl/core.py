from .corelib import Atom, Type, NoOp, Chain

HEADER = '''
#include <iostream>
#include <fstream>
#include <string>
typedef long double number;
using namespace std;
'''

NAME_STACK = []

class Parser(object):

	@staticmethod
	def valid_name(string):
		return string and all(c.isalnum() for c in '_' for c in string)

	def __init__(self, string):
		self.string = string
		self.token = None
		self.begin = 0
		self.end = 0
		self.name_stack = list(NAME_STACK)
		self.location_stack = []

		self.next()

	def push_location(self):
		self.location_stack.append((self.begin, self.end))

	def pop_location(self):
		self.begin, self.end = self.location_stack.pop()

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
		return self.begin >= len(self.string)

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

		self.begin = self.end

		while self.char and not self.char.isspace():
			self.end += 1

		self.token = self.string[self.begin:self.end]

		return last_token

	def consume(self, token):
		if self.token == token:
			return self.next()

	def parse_ast(self, base_ast_cls):
		for cls in base_ast_cls.instances:
			ast = cls.parse(self)
			if ast is not None:
				return ast

		raise SyntaxError('Expected %s %s' % (
				base_ast_cls.__name__, self.location_message))

	def parse_name_token(self):
		if self.valid_name(self.token):
			return self.next()

		raise SyntaxError('Expected name ' + self.location_message)

	def parse_atom(self):
		return self.parse_ast(Atom)

	def parse_atom_of_type(self, type_):
		self.push_location()
		atom = self.parse_atom()

		if atom.type != type_ and atom.type not in type_.supers:
			self.pop_location()
			raise SyntaxError(
					'Expected atom of type %s, but got one of type %s %s' % (
							type_, atom.type, self.location_message))
		return atom

	def parse_type(self):
		return self.parse_ast(Type)

	def parse_many_atoms(self, to_completion=False):
		expression = NoOp()
		try:
			while True:
				expression = Chain(expression, self.parse_atom())
		except SyntaxError:
			if to_completion and not self.done:
				raise
		return expression

	def parse_all(self):
		return self.parse_many_atoms(to_completion=True)

	def translate(self):
		return '%s\nint main(int argc, char** argv){%s;}\n' % (
				HEADER, self.parse_all())

	def __getitem__(self, key):
		for name, type_ in reversed(self.name_stack):
			if name == key:
				return type_
		raise SyntaxError('Name %s is not declared in this scope %s' % (
				key, self.location_message))
