#!/usr/bin/env python
# `python -m unittest unittest_truth_equality.TruthTest`
import unittest


class TruthTest(unittest.TestCase):
    # evaluate true value
    def testFailUnless(self):
        self.failUnless(True)

    def testAssertTrue(self):
        self.assertTrue(True)
        # self.assertEqual(0, int('0'))
        self.assertIs('  \n\n\n'.strip(), '')
        print(
            '\nContent Unit Counts:  \n  Puppet Module: 2'
            '\n\n\n'.split('Puppet Module:')[1]
        )
        print('\nContent Unit Counts:  \n\n\n'.split('Puppet Module:'))

    # evaluate false value,
    def testFailIf(self):
        self.failIf(False)

    def testAssertFalse(self):
        self.assertFalse(False)

    # test equality of two values
    def testEqual(self):
        self.failUnlessEqual(1, 3-2)

    # failure test
    def testNotEqual(self):
        self.failIfEqual(2, 3-1)

    # test for near equality of floating point numbers
    def testAlmostEqual(self):
        self.failUnlessAlmostEqual(1.1, 3.3-2.0, places=0)
        self.assertTrue(1.1 == (3.3-2.0), '3.3-2.0 is not exactly the 1.1')

if __name__ == '__main__':
    unittest.main()
