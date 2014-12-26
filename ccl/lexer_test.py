from unittest import TestCase, main
from .lexer import Token, Lexer

class LexerTestCase(TestCase):
  def testAll(self):
    text = "24.3 55 name 'string' +"
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
                type='EOF',
                value=None,
                text=text,
                mark=23),
        ],
        list(Lexer(text)))

if __name__ == '__main__':
  main()
