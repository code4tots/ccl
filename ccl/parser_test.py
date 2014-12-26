from unittest import TestCase, main
from .lexer import Lexer
from .parser import Parser

class ParserTestCase(TestCase):
  def testExpect(self):
    parser = Parser(Lexer("1234"))
    self.assertRaises(
      SyntaxError,
      parser.expect, 'NAME')

if __name__ == '__main__':
  main()
