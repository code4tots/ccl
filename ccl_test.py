import unittest, ccl, os

try:
  from unittest import mock
except ImportError:
  import mock


class ShellServiceTest(unittest.TestCase):

  def test_ls(self):
    self.assertItemsEqual(ccl.X.ls(), os.listdir())

if __name__ == '__main__':
  unittest.main()
