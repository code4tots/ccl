class Thunk(object):
  def __eq__(self, other):
    return type(self) == type(other) and self.__dict__ == other.__dict__

class Assignable(Thunk):
  pass

class Assign(Thunk):
  def __init__(self, lhs_thunk, rhs_thunk):
    self.lhs_thunk = lhs_thunk
    self.rhs_thunk = rhs_thunk

  def __call__(self, context):
    self.lhs_thunk.assign(context, self.rhs_thunk)

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

  def assign(self, context, value_thunk):
    context[self.name] = value = value_thunk(context)
    return value

class GetAttribute(Assignable):
  def __init__(self, owner_thunk, attribute_name):
    self.owner_thunk = owner_thunk
    self.attribute_name = attribute_name

  def __call__(self, context):
    return getattr(self.owner_thunk(context), self.attribute_name)

  def assign(self, context, value_thunk):
    setattr(self.owner_thunk(context), self.attribute_name, value_thunk(context))

class FunctionCall(Thunk):
  def __init__(self, f, args):
    self.f = f
    self.args = args

  def __call__(self, context):
    f = self.f(context)
    args = [arg(context) for arg in self.args]
    return f(*args)

