class Context(object):
  def __init__(self, parent):
    self._parent = parent
    self._table = dict()

  def __getitem__(self, key):
    return self._table[key] if key in self._table else self._parent[key]

  def __setitem__(self, key, value):
    self._table[key] = value


def evaluate(context, thunk):

  if isinstance(thunk, (int, float)):
    return thunk

  elif isinstance(thunk, str):
    return context[thunk]

  elif isinstance(thunk, list):
    macro = evaluate(context, thunk[0])
    return macro(context, thunk[1:])

  else:
    raise TypeError('Thunks must be int, float, str or list but found %r' % type(thunk))


BASE_CONTEXT = dict()

def register(name):
  def wrappper(macro):
    BASE_CONTEXT[name] = macro
    return macro
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

