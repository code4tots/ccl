import unittest
from . import core, corelib

class ParserTest(unittest.TestCase):
	def testParser(self):
		self.assertEqual(
			['a', 'b', 'c'],
			list(core.Parser('a b c')))

	def testNumberLiteralParse(self):
		self.assertEqual(
			corelib.NumberLiteral('55'),
			core.Parser('55').parse_atom())

	def testStringLiteralParse(self):
		self.assertEqual(
			corelib.StringLiteral('55'),
			core.Parser(':55').parse_atom())

if __name__ == '__main__':
	unittest.main()
