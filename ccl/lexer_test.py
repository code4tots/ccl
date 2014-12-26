from unittest import TestCase, main
from .lexer import Token, Lexer

class LexerTestCase(TestCase):

  def testOne(self):
    text = "1234"
    self.assertEqual(
        [
            Token(
                type='INT',
                value=1234,
                text=text,
                mark=0),
            Token(
                type='EOF',
                value=None,
                text=text,
                mark=4),
        ],
        list(Lexer(text)))

  def testAll(self):
    text = "24.3 55 name 'string' + if"
    self.assertEqual(
        [
            Token(
                type='FLOAT',
                value=24.3,
                text=text,
                mark=0),
            Token(
                type='INT',
                value=55,
                text=text,
                mark=5),
            Token(
                type='NAME',
                value='name',
                text=text,
                mark=8),
            Token(
                type='STRING',
                value='string',
                text=text,
                mark=13),
            Token(
                type='+',
                value='+',
                text=text,
                mark=22),
            Token(
                type='if',
                value='if',
                text=text,
                mark=24),
            Token(
                type='EOF',
                value=None,
                text=text,
                mark=26),
        ],
        list(Lexer(text)))

if __name__ == '__main__':
  main()
