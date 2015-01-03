class Context(object):
  def __init__(self, parent):
    self._parent = parent
    self._table = dict()

  def __getitem__(self, key):
    return self._table[key] if key in self._table else self._parent[key]

  def __setitem__(self, key, value):
    self._table[key] = value


class Object(object):
  def __init__(self, value):
    self.value = value

class Number(Object):
  def evaluate(self, context):
    return self

class String(Object):
  def evaluate(self, context):
    return context[self.value]

class List(Object):
  def evaluate(self, context):
    macro = self.value[0].evaluate(context)
    return macro(context, self.value[1:])

class Map(Object):
  pass

class Macro(Object):
  def __call__(self, context, argument_thunks):
    return self.value(context, argument_thunks)

BASE_CONTEXT = dict()

def register(name):
  def wrappper(macro):
    result = BASE_CONTEXT[name] = Macro(macro)
    return result
  return wrappper

@register('call-method')
def _(context, args):
  instance_thunk, method_name, method_arg_thunks = args
  instance = evaluate(context, instance_thunk)
  method_args = [evaluate(context, arg) for arg in method_arg_thunks]
  return getattr(instance, method_name)(*method_args)

@register('get-attribute')
def _(context, args):
  instance_thunk, attribute_name = args
  return getattr(evaluate(context, instance_thunk), attribute_name)

