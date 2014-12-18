#!/usr/bin/python
import os, sys
from ply import lex, yacc

start = 'command'
tokens = ('NUMBER', 'NAME', 'STRING', 'AND', 'OR', 'LPAR', 'RPAR', 'PIPE',
  'SEMICOLON')
t_ignore = ' \n\t'
precedence = (
  ('left', 'SEMICOLON'),
  ('left', 'OR'),
  ('left', 'AND'),
  ('left', 'PIPE'),)
t_LPAR = r'\('
t_RPAR = r'\)'
t_AND = r'\&\&'
t_OR = r'\|\|'
t_PIPE = r'\|'
t_SEMICOLON = r'\;'
def t_NUMBER(t): r'\d+\.?\d*'; t.value = Number(t.value); return t
def t_NAME(t): r'(?!\d)\w+'; t.value = Name(t.value); return t
def t_STRING(t): r'\"(?:\\\"|[^"])*\"'; t.value = String(t.value); return t
def p_number(p): "atom : NUMBER"; p[0] = p[1]
def p_name(p): "atom : NAME"; p[0] = p[1]
def p_string(p): "atom : STRING"; p[0] = p[1]
def p_parenthesis(p): "atom : LPAR command RPAR"; p[0] = p[2]
def p_atoms0(p): "atoms : atom"; p[0] = [p[1]]
def p_atoms1(p): "atoms : atoms atom"; p[0] = p[1]; p[0].append(p[2])
def p_atoms(p): "command : atoms"; p[0] = Command(p[1])
def p_pipe(p): "command : command PIPE command"; p[0] = Pipe([p[1], p[3]])
def p_sc(p): "command : command SEMICOLON command"; p[0] = Semicolon([p[1], p[3]])
lexer = lex.lex()
parser = yacc.yacc()
def parse(string): return parser.parse(string, lexer=lexer)

class Thunk(object):
  def __repr__(self):
    return type(self).__name__ + '(' + super(Thunk, self).__repr__() + ')'
class Number(Thunk, float):
  def eval(self, context): return self
class Name(Thunk, str):
  def eval(self, context): return context[self]
class String(Thunk, str):
  def eval(self, context): return eval(self)
class Command(Thunk, list):
  def eval(self, context, *args):
    return self[0].eval(context)(*(args + tuple(arg.eval(context) for arg in self[1:])))
class Pipe(Thunk, list):
  def eval(self, context, *args):
    lhs, rhs = self
    return rhs.eval(context, lhs.eval(context), *args)
class Semicolon(Thunk, list):
  def eval(self, context, *args):
    lhs, rhs = self
    lhs.eval(context)
    return rhs.eval(context, *args)

context = dict()
def register(name=None):
  def inner(f): context[name or f.__name__] = f; return f
  return inner
@register()
def cat(file_name):
  with open(file_name) as f: return f.read()
@register()
def printf(string, *args): return string % args
@register()
def ccl(string): return parse(string).eval(context)
@register()
def echo(value): return value
@register('print')
def print_(value): print(value); return value
@register()
def ls(): return os.listdir()
@register()
def add(lhs, rhs): return lhs + rhs

if __name__ == '__main__': ccl(sys.stdin.read())
