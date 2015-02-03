import re, collections, io, sys

header = '''
#include <string>
using namespace std;
'''

def nt(s): return collections.namedtuple('x', s)

class Stream(object):
	def __init__(self, string):
		self.gen = iter(re.sub(r'#[^\n]*\n', '\n', string).split() + [None])
		self.token = next(self.gen)

	def next(self):
		last_token = self.token
		self.token = next(self.gen)
		return last_token

	def consume(self, value):
		if self.token == value:
			return self.next()

ast_classes = []
variable_types = []

class AstMetaclass(type):
	def __init__(self, class_name, super_classes, class_dict):
		ast_classes.append(self)

class Ast(AstMetaclass('BaseAst', (), {})):
	pass

def parse(s):
	for ast_class in ast_classes:
		if hasattr(ast_class, 'parse'):
			result = ast_class.parse(s)
			if result is not None:
				return result

def force_parse(s):
	result = parse(s)
	if result is None:
		raise SyntaxError(s.token)
	return result

def translate(string):
	return str(Chain.parse(Stream(string)))

class Bind(nt('name variable_type')):
	def __enter__(self):
		variable_types.append((self.name, self.variable_type))

	def __exit__(*_):
		variable_types.pop()

class Chain(nt('lhs rhs')):
	@property
	def type(self):
		return self.rhs.type

	@staticmethod
	def parse(s):
		lhs = parse(s)
		if lhs is not None:
			rhs = parse(s)
			return lhs if rhs is None else Chain(lhs,rhs)

	def __str__(self):
		return '([](%s a,%s b){return b;})(%s,%s)' % (
				self.lhs.type, self.rhs.type, self.lhs, self.rhs)

class Number(Ast, str):
	type = 'long double'

	@staticmethod
	def parse(s):
		if s.token and all(c.isdigit() or c in '+-.' for c in s.token):
			return Number(s.next())

class Name(Ast, str):
	@property
	def type(self):
		for name, variable_type in reversed(variable_types):
			if self == name:
				return variable_type
		raise ValueError(self)

	@staticmethod
	def parse(s):
		if s.token and all(c.isalnum() and c in '_' for c in s.token):
			return Name(s.next())

class String(Ast, str):
	type = 'string'

	@staticmethod
	def parse(s):
		if s.token and s.token.startswith(':'):
			return String(s.next()[1:])

	def __str__(self):
		return '"' + self + '"'

class StringStream(Ast, tuple):
	type = 'string'

	@staticmethod
	def parse(s):
		if s.consume('.('):
			values = []
			while not s.consume(')'):
				values.append(force_parse(s))
			return StringStream(values)

	def __str__(self):
		return '([](%s){ostringstream ss;%s;return ss.str();})(%s)' % (
				','.join('%s x%d' % (v.type, i) for i, v in enumerate(self)),
				';'.join('ss<<x%d' for i in range(len(self))),
				','.join(map(str, self)))

# if __name__ == '__main__':
# 	sys.stdout.write(translate(sys.stdin.read()))

print translate('.( :hi )')
