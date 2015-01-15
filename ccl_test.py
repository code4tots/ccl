#!/usr/bin/python
import ccl, unittest

class CclTest(unittest.TestCase):

	def test_lex(self):
		self.assertItemsEqual(
				['(', 'ax', '2', ')'],
				ccl.lex(' (ax 2) '))

	def test_parse(self):
		self.assertEqual(
				['ls'],
				ccl.parse(ccl.lex('ls')))

		self.assertEqual(
				['cat', ['ls', '.']],
				ccl.parse(ccl.lex('cat (ls .)')))

if __name__ == '__main__':
	unittest.main()
