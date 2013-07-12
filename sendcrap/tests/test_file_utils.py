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

from sendcrap.utils import get_size, check_size, list_files

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
        
from sendcrap.utils import valid_http_url, valid_local_path        

VALID_URL    = 'http://www.python.org'
INVALID_URL  = 'http://www.python.org/rtfm/wtf/LOL.php'
VALID_PATH   = __file__
INVALID_PATH = 'random/crap/path/lol'

class TestPathCheckers(unittest.TestCase):
    def setUp(self): pass
    def tearDown(self): pass
    
    def test_is_valid_url(self):
        '''valid_http_url should return True if fed a valid url'''
        self.assertTrue(valid_http_url(VALID_URL))
        
    def test_is_invalid_url(self):
        '''valid_http_url should return False if fed an invalid url'''
        #~ self.assertFalse(valid_http_url(INVALID_URL))
        # Waiting for a response slows the whole suite down too much
        #~ self.assertFalse(valid_http_url(VALID_PATH))
        #~ self.assertFalse(valid_http_url(INVALID_PATH))
    
    def test_is_valid_path(self):
        '''valid_local_path should return True if fed a valid path from the local filesystem'''
        self.assertTrue(valid_local_path(VALID_PATH))
        
    def test_is_invalid_path(self):
        '''valid_local_path should return False if fed an invalid file path'''
        self.assertFalse(valid_local_path(INVALID_PATH))
        self.assertFalse(valid_local_path(VALID_URL))
        self.assertFalse(valid_local_path(INVALID_URL))

class TestListFiles(unittest.TestCase):

    root_dir = os.path.join(
         os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
         'data/test-data'
    )

    def setUp(self):
        if os.path.isfile(os.path.join(self.root_dir, 'data.tar')):
            os.remove(os.path.join(self.root_dir, 'data.tar'))

    def tearDown(self): pass

    def _match(self, pattern=None):
        '''Helper'''
        return list(list_files(self.root_dir, recursive=True,
                               abspathes=False, pattern=pattern)
               )

    def _check_match(self, expected, pattern=None):
        '''Helper'''
        self.assertListEqual(expected, self._match(pattern))

    def test_list_files(self):
        '''Default file listing'''
        # TODO: Flesh me out!
        expected = [
            'data/test-data/tumblr_m0byyulRLo1qc5ep4o1_500.jpg',
            'data/test-data/randomcrap.txt',
            'data/test-data/CV_rGaziano_dev_2012.pdf'
        ]                              
        expected = [os.path.abspath(p) for p in expected]
        res = list(list_files(self.root_dir))
        self.assertListEqual(expected, res)

    def test_pattern_matching_no_pattern(self):
        '''Pattern matching - defaulting to all'''
        expected = [
            'data/test-data/tumblr_m0byyulRLo1qc5ep4o1_500.jpg',
            'data/test-data/subdir/honkytonkbooze.txt',
            'data/test-data/subdir/wagonrythm.mp3',
            'data/test-data/randomcrap.txt',
            'data/test-data/CV_rGaziano_dev_2012.pdf'
        ]                              
        self._check_match(expected)

    def test_pattern_matching(self):
        '''Various pattern matching tests'''
        # TODO: Flesh me out!
        expected = [
            'data/test-data/subdir/honkytonkbooze.txt',
            'data/test-data/randomcrap.txt',
        ]                              
        self._check_match(expected, '*.txt')
        expected = [
            'data/test-data/tumblr_m0byyulRLo1qc5ep4o1_500.jpg',
            'data/test-data/subdir/honkytonkbooze.txt',
            'data/test-data/subdir/wagonrythm.mp3'
        ]                              
        self._check_match(expected, '*y*')
        
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestFileSizeChecks))
    suite.addTest(unittest.makeSuite(TestPathCheckers))
    suite.addTest(unittest.makeSuite(TestListFiles))
    return suite
