from unittest import TestCase, main
from . import thunk

class ThunkTestCase(TestCase):
  def testThunkEquality(self):
    self.assertEqual(
        thunk.Literal('hi'),
        thunk.Literal('hi'))

  def testThunkInequality(self):
    self.assertNotEqual(
        thunk.Name('hi'),
        thunk.Literal('hi'))

if __name__ == '__main__':
  main()
