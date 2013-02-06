#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
File-size checking test file. 
"""
import os
import unittest

TEST_DATA_DIR = os.path.join("data", "test-data")
TEST_FILES    = [os.path.join(TEST_DATA_DIR, 'randomcrap.txt'),
                 os.path.join(TEST_DATA_DIR, 
                    'tumblr_m0byyulRLo1qc5ep4o1_500.jpg'),
                 os.path.join(TEST_DATA_DIR, 'subdir', 
                    'wagonrythm.mp3')]

TEST_SINGLE_SIZE = 1010624 # Size (in bytes) of wagonrythm.mp3
TEST_MULTIPLE_SIZE = 1085283
TEST_MAX_SIZE = TEST_SINGLE_SIZE + TEST_MULTIPLE_SIZE 

from sendcrap.utils import get_size, check_size
        
class TestFileSizeChecks(unittest.TestCase):
    '''File size checking tests'''
    def setUp(self): pass        
    def tearDown(self): pass
    
    def test_get_file_size(self):
        '''utils.get_size() should return an accurate file size'''
        self.assertTrue(get_size(TEST_FILES[2]), TEST_SINGLE_SIZE)
        
    def test_get_file_size_multiple(self):
        '''utils.get_size() should return an accurate size when given multiple files'''
        self.assertTrue(get_size(*TEST_FILES), TEST_MULTIPLE_SIZE)
    
    def test_check_size(self):
        '''utils.check_size, single file'''
        self.assertTrue(check_size(TEST_MAX_SIZE, TEST_FILES[2]))
        self.assertFalse(check_size(666, TEST_FILES[2]))
        
    def test_check_size_multiple(self):
        '''utils.check_size, multiple files'''
        self.assertTrue(check_size(TEST_MAX_SIZE, TEST_FILES[2]))
        self.assertFalse(check_size(TEST_SINGLE_SIZE, *TEST_FILES))
        
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestFileSizeChecks))
    return suite
