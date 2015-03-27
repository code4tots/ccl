import collections

def NamedTuple(fields):
  return collections.namedtuple('NamedTuple', fields)
