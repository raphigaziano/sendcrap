#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
Compression test file.
Test the file archiving/compression utilities. 
"""
import unittest

class TestCompress(unittest.TestCase):
    '''Archiving/Compression Tests'''
    def setUp(self): pass
    def tearDown(self): pass
    
    #~ def test_build_archive(self):
        #~ '''A single archive should be built into the target directory'''
        #~ self.fail()
        

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestCompress))
    return suite
