import unittest, ccl

try:
  from unittest import mock
except ImportError:
  import mock


class ContextTest(unittest.TestCase):

  def testDirectVariable(self):
    context = ccl.Context(dict())
    context['key'] = 'value'
    self.assertEqual('value', context['key'])

  def testParentVariable(self):
    parent = ccl.Context(dict())
    child = ccl.Context(parent)
    parent['key'] = 'value'
    self.assertEqual('value', child['key'])


class EvaluateTest(unittest.TestCase):

  def setUp(self):
    self._context = ccl.Context({'x' : 'hi', 'macro': mock.Mock()})

  def evaluate(self, thunk):
    return ccl.evaluate(self._context, thunk)

  def testLiteral(self):
    self.assertEqual(4.0, self.evaluate(4.0))

  def testName(self):
    self.assertEqual('hi', self.evaluate('x'))

  def testMacro(self):
    self.evaluate(['macro', 'arg1', 'arg2'])
    self._context['macro'].assert_called_with(self._context, ['arg1', 'arg2'])

  def testInvalidThunkType(self):
    self.assertRaises(TypeError, self.evaluate, dict())


class BaseContextTest(unittest.TestCase):

  def setUp(self):
    self._context = ccl.Context(ccl.BASE_CONTEXT)

  def evaluate(self, thunk):
    return ccl.evaluate(self._context, thunk)

  def testCallMethod(self):
    self._context['a_list'] = [1, 2, 3]
    self.evaluate(['call-method', 'a_list', 'append', [4]])
    self.assertEqual([1, 2, 3, 4], self._context['a_list'])

  def testGetAttribute(self):

    class Sample(object):
      pass

    sample = Sample()
    sample.attribute = 5

    context = ccl.Context(ccl.BASE_CONTEXT)
    context['sample'] = sample

    self.assertEqual(5, ccl.evaluate(context, ['get-attribute', 'sample', 'attribute']))


if __name__ == '__main__':
  unittest.main()
