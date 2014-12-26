class Thunk(object):
  def __eq__(self, other):
    return type(self) == type(other) and self.__dict__ == other.__dict__

class Assignable(Thunk):
  pass

class Literal(Thunk):
  def __init__(self, value):
    self.value = value

  def __call__(self, context):
    return self.value

class Name(Assignable):
  def __init__(self, name):
    self.name = name

  def __call__(self, context):
    return context[self.name]

  def assign(self, context, value):
    context[self.name] = value
    return value

class FunctionCall(Thunk):
  def __init__(self, f, args):
    self.f = f
    self.args = args

  def __call__(self, context):
    f = self.f(context)
    args = [arg(context) for arg in self.args]
    return f(*args)

