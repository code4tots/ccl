#!/usr/bin/python
import ccl, unittest, io, sys, os

try:                from StringIO import StringIO
except ImportError: from io       import StringIO

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

	def test_execute(self):
		self.assertItemsEqual(
				os.listdir(os.getcwd()),
				ccl.execute(['ls'], ccl.CCL_BUILTINS))

	def test_repl(self):
		sys.stdin = in_ = StringIO("cwd")
		sys.stdout = out = StringIO()
		ccl.repl()
		self.assertEqual(out.read(), "/Users/math4tots/git/hub/ccl\n")


if __name__ == '__main__':
	unittest.main()
