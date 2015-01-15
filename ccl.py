#!/usr/bin/python
import re

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

def execute(thunk):
	pass

def run(file_):
	buffer_ = ''

	for line in file_:
		buffer_ += line
		if tokens.count('(') == tokens.count(')'):
			execute(parse(tokens))
			buffer_ = ''
