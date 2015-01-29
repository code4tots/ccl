import collections, sys

header = """
#include <cassert>
#include <algorithm>
#include <regex>
#include <utility>
#include <iostream>
#include <fstream>
#include <sstream>
#include <streambuf>
#include <string>
#include <vector>
#include <deque>
#include <map>
#include <set>
#include <unordered_map>
#include <unordered_set>
#include <array>
#include <tuple>
#include <queue>
using namespace std;
"""

def nt(s): return collections.namedtuple('x', s)

class Stream(object):
	def __init__(self, string):
		self.gen = iter(string.split() + [None])
		self.token = next(self.gen)

	def next(self):
		last = self.token
		self.token = next(self.gen)
		return last

	def consume(self, val):
		if self.token == val:
			return self.next()

types = []
asts = []

class Bind(nt('name, value_type')):
	def __enter__(self):
		types.append((self.name, self.value_type))

	def __exit__(self, type, value, traceback):
		types.pop()

def ast(a): asts.append(a); return a

def parse(s):
	if s.token is not None:
		for a in asts:
			r = a.parse(s)
			if r is not None:
				return r

class Chain(nt('lhs rhs')):
	@property
	def type(self): return self.rhs.type if self.rhs else self.lhs

	@staticmethod
	def parse(s):
		lhs = parse(s)
		if lhs:
			rhs = Chain.parse(s)
			return Chain(lhs, rhs) if rhs else lhs

	def __str__(self):
		return '((%s), (%s))' % (self.lhs, self.rhs) if self.rhs else str(self.lhs)

def translate(s):
	return '%s\nint main(){%s;}\n' % (header, str(Chain.parse(Stream(s))))

@ast
class Number(str):
	type = 'long double'

	@staticmethod
	def parse(s):
		if s.token != '.' and all(c.isdigit() or c in '+-.' for c in s.token):
			tok = s.next()
			if '.' not in tok:
				tok += '.0'
			return Number(tok+'L')

@ast
class String(str):
	type = 'string'

	@staticmethod
	def parse(s):
		if s.token.startswith("'"):
			return String(s.next()[1:])

	def __str__(self):
		return '"' + self + '"'

@ast
class Name(str):
	@property
	def type(self):
		for name, value_type in types:
			if self == name:
				return value_type
		raise NameError('undefined name: ' + self)

	@staticmethod
	def parse(s):
		if all(c.isalnum() or c in '_' for c in s.token):
			return Name(s.next())

@ast
class Print(nt('x')):
	@property
	def type(self): return self.x.type

	@staticmethod
	def parse(s):
		if s.consume('.p'):
			return Print(parse(s))

	def __str__(self):
		return '([](%s x){cout << x; return x;})(%s)' % (self.x.type, self.x)

@ast
class Read(nt('type')):
	@staticmethod
	def parse(s):
		if s.consume('.r'):
			return Read(s.next())

	def __str__(self):
		return '([](){%s x;cin>>x;return x;})()' % (self.type)

@ast
class Space(object):
	type = 'string'

	@staticmethod
	def parse(s):
		if s.consume('.s'):
			return Space()

	def __str__(self):
		return '" "'

@ast
class StringStream(nt('xs')):
	type = 'string'

	@staticmethod
	def parse(s):
		if s.consume(':'):
			xs = []
			while not s.consume(';'):
				xs.append(parse(s))
			return StringStream(xs)

	def __str__(self):
		return '([&](){ostringstream _ss;%s;return _ss.str();})()' % ';'.join(
				'_ss << ' + str(x) for x in  self.xs)

@ast
class Let(nt('name value expr')):
	@property
	def type(self):
		with Bind(name, self.value.type):
			return self.expr.type

	@staticmethod
	def parse(s):
		if s.token.endswith('='):
			name = s.next()[:-1]
			value = parse(s)
			assert value is not None
			expr = Chain.parse(s)
			assert expr is not None
			return Let(name, value, expr)

	def __str__(self):
		with Bind(self.name, self.value.type):
			expr_str = str(self.expr)

		return '([&](%s %s){return %s;})(%s)' % (
				self.value.type, self.name, expr_str, self.value)

@ast
class Block(nt('x')):
	@property
	def type(self):
		return self.x.type

	@staticmethod
	def parse(s):
		if s.consume('{'):
			x = Chain.parse(s)
			assert s.consume('}')
			return Block(x)

	def __str__(self):
		return str(self.x)

if __name__ == '__main__':
	sys.stdout.write(translate(sys.stdin.read()))
