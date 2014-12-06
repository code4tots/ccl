"""A language's core should be its AST, and not include its grammar."""

class Node(object):
  def __init__(self, *args, **kwargs):
    for name, value in zip(self.attributes, args):
      setattr(self, name, value)
    self.init()

  def init(self):
    pass

  def execute(self, context):
    raise NotImplemented("This node's execute method has not been implemented")

class FunctionCall(Node):
  attributes = ('function', 'arguments')

class FunctionDefinition(Node):
  attributes = ('name', 'arguments', 'body')

class Assignment(Node):
  attributes = ('variable_name', 'value')

class Literal(Node):
  attributes = ('value',)
  def init(self):
    self.value = self.type(self.value)

class IntegerLiteral(Literal):
  type = int

class FloatingLiteral(Literal):
  type = float

