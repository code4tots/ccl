#!/usr/bin/python

"""Javascript-esque programming language.

types:
  - nil
  - bool
  - string
  - number
  - list
  - dict
  - builtin

Objects double as both data structures in the language and AST constructs for
the language.

The 'evaluate' method is called when the object is interpreted as an AST
construct.

The 'call' method is called when the object is interpreted as a macro/function.

Only dict and builtins can be interpreted as macro/function.

TODO:
  The way hashes are implemented right now, make calculating hashes expensive.
  Perhaps I could move to Ruby so that I don't have to worry about it myself.
  Or maybe I could supply a fix. But for now, I think it's ok to have an
  inefficient implementation.

"""

class Object(object):
  def __nonzero__(self):
    return self.__bool__()

  def evaluate(self, context):
    return self

class Nil(Object):
  name = 'nil'

  def __new__(cls):
    global nil

    if nil is None:
      nil = super(Nil, cls).__new__(cls)

    return nil

  def __bool__(self):
    return False

  def __str__(self):
    return 'nil'

class Bool(Object):
  name = 'bool'

  def __new__(cls, truthy):
    global true, false

    if truthy:
      if true is None:
        true = super(Bool, cls).__new__(cls)
        true.value = True
      return true

    else:
      if false is None:
        false = super(Bool, cls).__new__(cls)
        false.value = False
      return false

  def __bool__(self):
    return self.value

  def __str__(self):
    return 'true' if self.value else 'false'

class String(str, Object):
  name = 'string'

  def evaluate(self, context):
    return context[self]

class Number(float, Object):
  name = 'number'

class List(list, Object):
  name = 'list'

  def evaluate(self, context):
    return self[0].evaluate(context).call(context, self[1:])

  def __hash__(self):
    return hash(tuple(self))

class Dict(dict, Object):
  name = 'dict'

  def call(self, dynamic_context, arg_thunks):
    static_context = Context(self.get('__context__'))
    static_context[self.get('__context_name__')] = dynamic_context
    static_context[self.get('__args_name__')] = arg_thunks
    return self.get('__thunk__').evaluate(static_context)

  def get(self, key):
    if key in self:
      return self[key]
    elif '__prototype__' in self:
      return self['__prototype__']
    raise KeyError(key)

  def __hash__(self):
    return hash(tuple(self.items()))

class Builtin(Object):
  name = 'builtin'

  def __init__(self, macro):
    self.macro = macro

  def call(self, context, args):
    return self.macro(context, args)

nil = None
nil = Nil()
true = None
true = Bool(True)
false = None
false = Bool(False)
