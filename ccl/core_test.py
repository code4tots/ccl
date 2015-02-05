import unittest
from . import core

class CoreTest(unittest.TestCase):
	def testParser(self):
		self.assertEqual(
			['a', 'b', 'c'],
			list(core.Parser('a b c')))

if __name__ == '__main__':
	unittest.main()
