#!/usr/bin/env python
# Testing for Exceptions
# `python unittest_exception.py -v`, or
# `python -m unittest unittest_exception.ExceptionTest`
import unittest


def raises_error(*args, **kwds):
    print(args, kwds)
    raise ValueError('Invalid value: ' + str(args) + str(kwds))


class ExceptionTest(unittest.TestCase):

    def testTrapLocally(self):
        try:
            raises_error('a', b='c')
        except ValueError:
            pass
        else:
            self.fail('Did not see ValueError')

    def testFailUnlessRaises(self):
        """
        `failUnlessRaises()` makes the code more clear than
        trapping the exception yourself.
        """
        self.failUnlessRaises(ValueError, raises_error, 'a', b='c')

if __name__ == '__main__':
    unittest.main()
