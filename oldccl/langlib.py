from .core import *
from .corelib import *

class Reference(TypeTuple('type')):
	def __new__(cls, type):
		return (type if isinstance(type, Reference) else 
				super(Reference, cls).__new__(cls, type))

	def declare(self, inside):
		return self.type.declare('(&%s)' % (inside,))

class Deque(TypeTuple('type')):
	@staticmethod
	def parse(s):
		if s.consume('deque'):
			return Deque(s.parse_type())

	def declare(self, inside):
		return 'std::deque<' + self.type.declare('') + ' > ' + inside

class Ostream(SimpleType):
	name = 'ostream'

class Istream(SimpleType):
	name = 'istream'

class Ifstream(SimpleType):
	supers = SimpleType.supers + (Istream(),)
	name = 'ifstream'

class Ofstream(SimpleType):
	supers = SimpleType.supers + (Ostream(),)
	name = 'ofstream'

class Write(AtomTuple('stream value')):
	same_type_as = 'value'

	@staticmethod
	def parse(s):
		if s.consume('.write'):
			return Write(s.parse_atom_of_type(Ostream()), s.parse_atom())

	def __str__(self):
		return '([](%s,%s){stream << value;return value;}(%s,%s))' % (
				Reference(self.stream.type).declare('stream'),
				self.value.type.declare('value'),
				self.stream, self.value)

NAME_STACK.extend([
	('cout', Ostream()),
])
