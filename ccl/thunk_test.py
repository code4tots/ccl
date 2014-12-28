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

  def testName(self):
    context = {
        'a': 1337,
        'b': 9000}

    a_thunk = thunk.Name('a')
    b_thunk = thunk.Name('b')

    self.assertEqual(
        1337,
        a_thunk(context))

    a_thunk.assign(context, b_thunk)

    self.assertEqual(
        9000,
        a_thunk(context))

  def testFunctionCall(self):
    context = {'a': [1, 2, 3, 4, 5], 'len': len}

    function_thunk = thunk.FunctionCall(
        thunk.Name('len'),
        [thunk.Name('a')])

    self.assertEqual(
        5,
        function_thunk(context))

  def testGetAttribute(self):

    class Sample(object):
      pass

    context = {'sample': Sample()}

    thunk.Assign(
        thunk.GetAttribute(thunk.Name('sample'), 'attribute'),
        thunk.Literal('hi'))(context)

    self.assertEqual(
        'hi',
        thunk.GetAttribute(thunk.Name('sample'), 'attribute')(context))

if __name__ == '__main__':
  main()
