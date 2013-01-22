#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
File listing test file.
Test the file listing utilities with various arguments. 
"""
import unittest
import os

from sendcrap.args import _list_files as list_files

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
        '''list_files(dir) should return all files from dir'''
        pathes = [
            os.path.join(TEST_DATA_DIR, 'CV_rGaziano_dev_2012.pdf'),
            os.path.join(TEST_DATA_DIR, 'randomcrap.txt'),
            os.path.join(TEST_DATA_DIR, 'tumblr_m0byyulRLo1qc5ep4o1_500.jpg')
        ]
        files = list_files(TEST_DATA_DIR)
        self._check_pathes(pathes, files)

    def test_file_list_all_recursive(self):
        '''list_files(dir, walk=True) should browse directories recursively'''
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
        '''list_files(arbs=[...]) should return only the requested files'''
        pathes = [
            os.path.join(TEST_DATA_DIR, 'randomcrap.txt'),
            os.path.join(TEST_DATA_DIR, 'subdir', 'wagonwheel.mp3'),
            'setup.py',
            'sendcrap/tests/test_file_list.py'
        ]
        files = list_files(arbs=pathes)
        self._check_pathes(pathes, files)

    def test_file_list_arbitrary_plus_params(self):
        '''Any arbitrary files should be added to whatever other selection'''
        pathes = [
            os.path.join(TEST_DATA_DIR, 'CV_rGaziano_dev_2012.pdf'),
            os.path.join(TEST_DATA_DIR, 'randomcrap.txt'),
            os.path.join(TEST_DATA_DIR, 'tumblr_m0byyulRLo1qc5ep4o1_500.jpg'),
            'setup.py'
        ]
        files = list_files(TEST_DATA_DIR, arbs=['setup.py'])
        self._check_pathes(pathes, files)
        
        pathes = [
            os.path.join(TEST_DATA_DIR, 'tumblr_m0byyulRLo1qc5ep4o1_500.jpg'),
            'sendcrap/getfiles.py'
        ]
        files  = list_files(TEST_DATA_DIR, exts=['.jpg'], arbs=['sendcrap/getfiles.py'])
        self._check_pathes(pathes, files)
            
    def test_file_list_exts(self):
        '''list_files(dir, exts=[...]): all files returned should have the right extension(s)'''
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
        '''list_files(dir, walk=True, exts=[...]): combining recurive search and exts filtering'''
        pathes = [
            os.path.join(TEST_DATA_DIR, 'randomcrap.txt'),
            os.path.join(TEST_DATA_DIR, 'subdir', 'honkytonkbooze.txt')
        ]
        files  = list_files(TEST_DATA_DIR, walk=True, exts=['.txt'])
        self._check_pathes(pathes, files)
        
    def test_all_opts_at_once(self):
        '''Testing list_files() with all args set'''
        pathes = [
            os.path.join(TEST_DATA_DIR, 'randomcrap.txt'),
            os.path.join(TEST_DATA_DIR, 'subdir', 'honkytonkbooze.txt'),
            os.path.join('sendcrap', 'tests', 'test_file_list.py'),
            os.path.join('MANIFEST.in')
        ]
        files  = list_files(TEST_DATA_DIR, walk=True, exts=['.txt'],
            arbs = [os.path.join('sendcrap', 'tests', 'test_file_list.py'),
                    os.path.join('MANIFEST.in')])
        self._check_pathes(pathes, files)
        
    def test_recursive_plus_exts(self):
        '''list_files with recursion and filtered extensions'''
        expected = [os.path.join(TEST_DATA_DIR, 
                                 'subdir', 'wagonrythm.mp3')]
        self._check_pathes(expected, 
                           list_files(TEST_DATA_DIR, walk=True,
                                      exts=['.mp3']))

    def test_several_exts(self):
        '''list_files with recursion and filtered extensions'''
        expected = [
            os.path.join(TEST_DATA_DIR, 'randomcrap.txt'),
            os.path.join(TEST_DATA_DIR, 'subdir', 'honkytonkbooze.txt'),
            os.path.join(TEST_DATA_DIR, 'subdir', 'wagonrythm.mp3'),
            
        ]
        self._check_pathes(expected, 
                           list_files(TEST_DATA_DIR, walk=True,
                                      exts=['.txt', '.mp3']))
        
    def test_no_input(self):
        '''list_file() (No args) should return an empty list'''
        pathes = []
        files = list_files()
        self._check_pathes(pathes, files)
        
    
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestFilesList))
    return suite
