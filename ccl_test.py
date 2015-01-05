import unittest, ccl

try:
  from unittest import mock
except ImportError:
  import mock


class ObjectTest(unittest.TestCase):

  def testTruthiness(self):
    self.assertFalse(ccl.nil)
    self.assertFalse(ccl.false)
    self.assertTrue(ccl.true)


if __name__ == '__main__':
  unittest.main()
