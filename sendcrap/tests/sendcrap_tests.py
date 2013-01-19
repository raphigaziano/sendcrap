#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
Main test file.
Dynamically builds test suites out of all the other test files and run 
them all.
"""

import unittest
import os
import imp

suite = unittest.TestSuite()

# Dynamic building of the whole test suite
# BROKEN :(:(:(
for f in os.listdir(os.path.dirname(__file__)):
    if f == os.path.basename(__file__): continue
    if f == '__init__.py':              continue
    name, ext = os.path.splitext(f)
    if ext == '.py' and f.startswith('test'):
        #~ try:
            #~ # This will work if running the script directly,
            #~ # ie python app/tests/app_tests
            #~ test_module = __import__(name)
        #~ except ImportError:
            #~ # For some reason, nosetests needs this version
            #~ # (Which screws up the direct import)
            #~ test_module = __import__("sendcrap.tests.%s" % name, 
                                     #~ fromlist=["sendcrap", "tests"])
        test_module = __import__(name, 
                         globals=globals(),
                         fromlist=[name])
        suite.addTest(test_module.suite())

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite)
