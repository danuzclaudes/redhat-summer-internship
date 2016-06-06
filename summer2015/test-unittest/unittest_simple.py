#!/usr/bin/env python
import unittest


class SimpleTest(unittest.TestCase):
  def test(self):
    self.failUnless(True)

if __name__ == '__main__':
    unittest.main()
