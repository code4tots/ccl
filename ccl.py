#!/usr/bin/python
import re, io, os, sys

try: input = raw_input
except NameError: pass

def lex(string):
	return [token for token in re.findall(
			r'\s+|'
			r'\"(?:\\\"|[^"]*)\"|'
			r'[()]|'
			r'[^\s\"()]+',
			string) if token.strip()]

def parse(tokens):
	stack = [[]]
	for token in tokens:
		if   token == '(': stack.append([])
		elif token == ')': stack[-2].append(stack.pop())
		else: stack[-1].append(token)
	assert len(stack) == 1
	return stack[0]

class Runtime(object):

	def __init__(self, context):
		self._buffer = ''
		self._context = context

	def input(self, string):
		self._buffer += str(string)

	def execute(self):
		result = execute(parse(lex(self._buffer)), self._context)
		self._buffer = ''
		return result

	def complete(self):
		tokens = lex(self._buffer)
		return self._buffer and tokens.count('(') == tokens.count(')')

def run(file_):
	runtime = Runtime(CCL_BUILTINS)
	for line in file_:
		runtime.input(line)
		if runtime.complete():
			runtime.execute()

def repl():
	runtime = Runtime(CCL_BUILTINS)
	try:
		while True:
			runtime.input(input('>>> '))
			while not runtime.complete():
				runtime.input(input('... '))
			result = runtime.execute()
			if result is not None:
				print(result)
	except EOFError:
		pass

def execute(thunk, context):
	return (context[thunk] if isinstance(thunk, str) else
		      execute(thunk[0], context)(*thunk[1:]))

CCL_BUILTINS = dict()

def function(f):
	CCL_BUILTINS[f.__name__] = f
	return f

@function
def ls(path='.'):
	return os.listdir(path)

@function
def cwd():
	return os.getcwd()

if __name__ == '__main__':
	repl()
