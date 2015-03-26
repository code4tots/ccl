import collections

def NamedTuple(fields):
  return collections.namedtuple('NamedTuple', fields)


def overrides(interface_class):
  def overrider(method):
    if method.__name__ not in dir(interface_class):
      raise TypeError('method %r does not override %s' % (
          method.__name__,
          interface_class))
    return method
  return overrider
