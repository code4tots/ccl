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

def flatten(chain):
	return [chain.lhs] + ([] if chain.rhs is None else flatten(chain.rhs))

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

asts = []

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
			return Chain(lhs, rhs)

	def __str__(self):
		return '((%s), (%s))' % (self.lhs, self.rhs) if self.rhs else str(self.lhs)

def translate(s):
	return '%s\nint main(){%s;}\n' % (header, str(Chain.parse(Stream(s))))

@ast
class Print(nt('x')):
	@property
	def type(self): return self.x.type

	@staticmethod
	def parse(s):
		if s.consume('p'):
			return Print(parse(s))

	def __str__(self):
		return '([](%s x){cout << x; return x;})(%s)' % (self.x.type, self.x)

@ast
class Number(str):
	type = 'double'

	@staticmethod
	def parse(s):
		if s.token != '.' and all(c.isdigit() or c in '+-.' for c in s.token):
			return Number(s.next())

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
class StringStream(nt('xs')):
	type = 'string'

	@staticmethod
	def parse(s):
		if s.consume(':'):
			xs = flatten(Chain.parse(s))
			assert s.consume(';')
			return StringStream(xs)

	def __str__(self):
		return '([&](){ostringstream _ss;%s;return _ss.str();})()' % ';'.join(
				'_ss << ' + str(x) for x in  self.xs)

if __name__ == '__main__':
	sys.stdout.write(translate(sys.stdin.read()))
