#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
Recipients test file.
Test the retrieving of a recipients list.
"""
import unittest

class TestRecipients(unittest.TestCase):
    '''Archiving/Compression Tests'''
    def setUp(self): pass
    def tearDown(self): pass
        

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestRecipients))
    return suite
