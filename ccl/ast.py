from collections import namedtuple

class AstMetaclass(type):
	def __new__(mcs, name, bases, dict_):
		cls = super(AstMetaclass, mcs).__new__(mcs, name, bases, dict_)
		cls.ast_clss.append(cls)
		return cls

BaseAst = AstMetaclass('BaseAst', (), {
		'ast_clss': [],
		'parse': lambda self, s: None,
})

class Ast(BaseAst):
	def __new__(cls, *args, **kwargs):
		self = super(Ast, cls).__new__(cls, *args, **kwargs)
		if hasattr(self, 'same_type_as'):
			self.type = getattr(self, self.same_type_as).type
		return self

	def __eq__(self, other):
		return type(self) == type(other) and super(Ast, self).__eq__(other)

	def is_a(self, type_):
		return self.type == type_

class Type(Ast):
	pass

class PrimitiveType(Type, str):
	@staticmethod
	def parse(s):
		if s.token.startswith('$'):
			return PrimitiveType(s.next()[1:])

TypeType = PrimitiveType('type')
NumberType = PrimitiveType('number')
StringType = PrimitiveType('string')

PrimitiveType.type = TypeType

def TypeTuple(s):
	class TypeTuple(Type, namedtuple('TypeTuple', s)):
		pass
	return TypeTuple

class ListType(TypeTuple('value_type')):
	type = TypeType

	@staticmethod
	def parse(s):
		if s.consume('@list'):
			return ListType(s(TypeType))

class DictType(TypeTuple('key_type value_type')):
	type = TypeType

	@staticmethod
	def parse(s):
		if s.consume('@dict'):
			return DictType(s(TypeType), s(TypeType))

class Expression(Ast):
	pass

def ExpressionTuple(s):
	class ExpressionTuple(Expression, namedtuple('ExpressionTuple', s)):
		pass
	return ExpressionTuple

class Chain(ExpressionTuple('lhs rhs')):
	same_type_as = 'rhs'

class NoOp(Expression):
	type = NumberType

	def __eq__(self, other):
		return type(self) == type(other)

assert TypeType == PrimitiveType('type')
assert Chain(NoOp(), NoOp()).type == NoOp().type == NumberType
assert NoOp() == NoOp()
assert Chain(NoOp(), NoOp()) == Chain(NoOp(), NoOp())

