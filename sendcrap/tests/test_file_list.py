#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
File listing test file.
Test the file listing utilities with various arguments. 
"""
import unittest
import os

from sendcrap.utils import list_files

TEST_DATA_DIR = os.path.join("data", "test-data")

class TestFilesList(unittest.TestCase):
    '''Archiving/Compression Tests'''
    def setUp(self): pass
    def tearDown(self): pass
    
    def _check_pathes(self, expected, received):
        '''Common helper for the individual tests''' 
        self.assertTrue(all([e in received for e in expected]))
        self.assertTrue(all([r in expected for r in received]))
    
    def test_file_list_all(self):
        '''All files from the directory should be listed if no args are provided'''
        pathes = [
            os.path.join(TEST_DATA_DIR, 'CV_rGaziano_dev_2012.pdf'),
            os.path.join(TEST_DATA_DIR, 'randomcrap.txt'),
            os.path.join(TEST_DATA_DIR, 'tumblr_m0byyulRLo1qc5ep4o1_500.jpg')
        ]
        files = list_files(TEST_DATA_DIR)
        self._check_pathes(pathes, files)

    def test_file_list_all_recursive(self):
        '''All files from all subdirectories if recursion is requested'''
        pathes = [
            os.path.join(TEST_DATA_DIR, 'CV_rGaziano_dev_2012.pdf'),
            os.path.join(TEST_DATA_DIR, 'randomcrap.txt'),
            os.path.join(TEST_DATA_DIR, 'tumblr_m0byyulRLo1qc5ep4o1_500.jpg'),
            os.path.join(TEST_DATA_DIR, 'subdir', 'wagonrythm.mp3'),
            os.path.join(TEST_DATA_DIR, 'subdir', 'honkytonkbooze.txt'),
        ]
        files = list_files(TEST_DATA_DIR, walk=True)
        self._check_pathes(pathes, files)
    
    def test_file_list_arbitrary(self):
        '''If arbitrary files and no dir are specified, then only the spec files should be returned'''
        pathes = [
            os.path.join(TEST_DATA_DIR, 'randomcrap.txt'),
            os.path.join(TEST_DATA_DIR, 'subdir', 'wagonwheel.mp3'),
            'setup.py',
            'sendcrap/tests/test_file_list.py'
        ]
        files = list_files(arb_files=pathes)
        self._check_pathes(pathes, files)

    def test_file_list_arbitrary_plus_params(self):
        '''Any arbitrary files should be added to whatever other selection'''
        pathes = [
            os.path.join(TEST_DATA_DIR, 'CV_rGaziano_dev_2012.pdf'),
            os.path.join(TEST_DATA_DIR, 'randomcrap.txt'),
            os.path.join(TEST_DATA_DIR, 'tumblr_m0byyulRLo1qc5ep4o1_500.jpg'),
            'setup.py'
        ]
        files = list_files(TEST_DATA_DIR, arb_files=['setup.py'])
        self._check_pathes(pathes, files)
        
        pathes = [
            os.path.join(TEST_DATA_DIR, 'tumblr_m0byyulRLo1qc5ep4o1_500.jpg'),
            'sendcrap/getfiles.py'
        ]
        files  = list_files(TEST_DATA_DIR, exts=['.jpg'], arb_files=['sendcrap/getfiles.py'])
        self._check_pathes(pathes, files)
            
    def test_file_list_exts(self):
        '''The files to be compressed should all have the provided extension'''
        # .txt
        pathes = [os.path.join(TEST_DATA_DIR, 'randomcrap.txt')]
        files  = list_files(TEST_DATA_DIR, exts=['.txt'])
        self._check_pathes(pathes, files)
        # .jpg
        pathes = [os.path.join(TEST_DATA_DIR, 'tumblr_m0byyulRLo1qc5ep4o1_500.jpg')]
        files  = list_files(TEST_DATA_DIR, exts=['.jpg'])
        self._check_pathes(pathes, files)
        # .pdf
        pathes = [os.path.join(TEST_DATA_DIR, 'CV_rGaziano_dev_2012.pdf')]
        files  = list_files(TEST_DATA_DIR, exts=['.pdf'])
        self._check_pathes(pathes, files)
        # .mp3
        pathes = [os.path.join(TEST_DATA_DIR, 'subdir', 'wagonrythm.mp3')]
        files  = list_files(os.path.join(TEST_DATA_DIR, 'subdir'), exts=['.mp3'])
        self._check_pathes(pathes, files)
        
    def test_file_list_exts_plus_recursive(self):
        '''Specified extension plus recursion'''
        pathes = [
            os.path.join(TEST_DATA_DIR, 'randomcrap.txt'),
            os.path.join(TEST_DATA_DIR, 'subdir', 'honkytonkbooze.txt')
        ]
        files  = list_files(TEST_DATA_DIR, walk=True, exts=['.txt'])
        self._check_pathes(pathes, files)
        
    def test_all_opts_at_once(self):
        '''Going wild!!!'''
        pathes = [
            os.path.join(TEST_DATA_DIR, 'randomcrap.txt'),
            os.path.join(TEST_DATA_DIR, 'subdir', 'honkytonkbooze.txt'),
            os.path.join('sendcrap', 'tests', 'test_file_list.py'),
            os.path.join('MANIFEST.in')
        ]
        files  = list_files(TEST_DATA_DIR, walk=True, exts=['.txt'],
            arb_files = [os.path.join('sendcrap', 'tests', 'test_file_list.py'),
                         os.path.join('MANIFEST.in')])
        self._check_pathes(pathes, files)
        
    def test_no_input(self):
        '''No input should return an empty list'''
        pathes = []
        files = list_files()
        self._check_pathes(pathes, files)
        
    
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestFilesList))
    return suite
