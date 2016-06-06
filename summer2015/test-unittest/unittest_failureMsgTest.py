#!/usr/bin/env python
# `python unittest_failureMsgTest.py -v`
import unittest


class OutcomesTest(unittest.TestCase):

    def testPass(self):
        return

    def testFail(self):
        self.failIf(True, 'failure msg goes here')

    def testError(self):
        raise RuntimeError('Test error!')

if __name__ == '__main__':
    unittest.main()
