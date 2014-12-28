from unittest import TestCase, main
from . import thunk
from .lexer import Lexer, Token
from .parser import Parser

class ParserTestCase(TestCase):

  def test_consume(self):
    text = '5.5 name'
    parser = Parser(Lexer(text))

    self.assertEqual(
        None,
        parser.consume('NAME'))

    self.assertEqual(
        Token(
          type='FLOAT',
          value=5.5,
          text=text,
          mark=0),
        parser.consume('FLOAT'))

    self.assertEqual(
        None,
        parser.consume('FLOAT'))

    self.assertEqual(
        'NAME',
        parser.consume('NAME').type)

  def test_expect(self):
    parser = Parser(Lexer('1234'))
    self.assertRaises(
      SyntaxError,
      parser.expect, 'NAME')

  def test_token_literal_expression(self):
    parser = Parser(Lexer('1234'))

    self.assertEqual(
        thunk.Literal(1234),
        parser.token_literal_expression('INT'))

  def test_name_expression(self):
    parser = Parser(Lexer('hi'))

    self.assertEqual(
        thunk.Name('hi'),
        parser.name_expression())

  def test_parenthetical_expression(self):
    parser = Parser(Lexer('(hi)'))

    self.assertEqual(
        thunk.Name('hi'),
        parser.parenthetical_expression())

    parser = Parser(Lexer('hi'))

    self.assertEqual(
        None,
        parser.parenthetical_expression())

  def test_atom_expression(self):
    parser = Parser(Lexer('(hi)'))

    self.assertEqual(
        thunk.Name('hi'),
        parser.atom_expression())

    parser = Parser(Lexer('hi'))

    self.assertEqual(
        thunk.Name('hi'),
        parser.atom_expression())


if __name__ == '__main__':
  main()
