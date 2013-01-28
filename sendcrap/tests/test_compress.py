#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
Compression test file.
Test the file archiving/compression utilities. 
"""
import unittest
import os
import tarfile
from sendcrap.tar import write

TEST_DATA_DIR = os.path.join("data", "test-data")
TAR_PATH      = os.path.join(TEST_DATA_DIR, "test-data.tar")
TEST_FILES    = [os.path.join(TEST_DATA_DIR, 'randomcrap.txt'),
                 os.path.join(TEST_DATA_DIR, 'tumblr_m0byyulRLo1qc5ep4o1_500.jpg'),
                 os.path.join(TEST_DATA_DIR, 'subdir', 'wagonrythm.mp3')]


class TestCompress(unittest.TestCase):
    '''Archiving/Compression Tests'''
    def setUp(self): pass
        
    def tearDown(self):
        if os.path.isfile(TAR_PATH): os.remove(TAR_PATH)
    
    def test_build_archive(self):
        '''A single archive should be built into the target directory'''
        write(TEST_DATA_DIR, *TEST_FILES)
        self.assertTrue(os.path.isfile(TAR_PATH))
        
    def test_nonexistent_filenames(self):
        '''Trying to pack non-existent filenames should raise an OSError'''
        self.assertRaises(OSError, write, TEST_DATA_DIR,
            *[os.path.join(TEST_DATA_DIR, 'imnotthere.txt'), 
              'meneither.pdf'])
              
    def test_invalid_file_args(self):
        '''Passing an actual list to tar.write instead of varargs should raise a TypeError'''
        self.assertRaises(TypeError, write, TEST_DATA_DIR, TEST_FILES)
        
    def test_archive_contents(self):
        '''Testing archive contents'''
        write(TEST_DATA_DIR, *TEST_FILES)
        with tarfile.open(TAR_PATH, 'r') as tf:
            tf_contents = [os.path.normpath(f) for f in tf.getnames()]
            self.assertTrue(len(tf_contents) == len(TEST_FILES))
            self.assertTrue(all([f in TEST_FILES for f in tf_contents]))
            self.assertTrue(all([f in tf_contents for f in TEST_FILES]))
        
        
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestCompress))
    return suite
