#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
CLI Arg parsing test file
"""
import sys
try:
    from StringIO import StringIO #py2
except ImportError: # py3
    try : from io import cStringIO as StringIO
    except ImportError: from io import StringIO
import unittest
from sendcrap.args import _parser as parser, process_args
#~ from sendcrap.args import InvalidArgumentsException
# Replacing args conf with the dummy sample config file
from sendcrap import args
import conf_sample as conf
args.conf = conf

def _args(args):
    '''Common helper for the individual tests'''
    return parser.parse_args(args.split())

class TestArgParser(unittest.TestCase):
    '''Command line processing tests'''
    def setUp(self):
        self.buffer_ = StringIO()
    
    def tearDown(self): pass
    
    # def test_...

class TestArgParserInput(TestArgParser):
    '''Error handling related to received arguments'''
    def _assertSysExit(self, f, *args, **kwargs):
        '''
        Common helper.
        Silence stderr while checking for a SysExit exception.
        '''
        stderr, sys.stderr = sys.stderr, self.buffer_
        try:
            self.assertRaises(SystemExit, f, *args, **kwargs)
        except SystemExit: pass
        sys.stderr = stderr
        
    def test_random_input(self):
        '''Argument parser should die if given random input'''
        self._assertSysExit(_args, 'iukjb hj ç_y')
        
    def test_non_existent_flag(self):
        '''Argument parser should die if given inexistant flags'''
        self._assertSysExit(_args, '-o')
        self._assertSysExit(_args, '-gjk')
        self._assertSysExit(_args, '-o -g -t')
        # Non existent along with correct flags:
        self._assertSysExit(_args, '-ro')
        self._assertSysExit(_args, '-r -o')

    def test_non_existent_opts(self):
        '''Argument parser should die if given inexistant options'''
        self._assertSysExit(_args, '--oop')
        self._assertSysExit(_args, '--pool --poop')
        # Non existent along with correct opts:
        self._assertSysExit(_args, '--summinwrong 42 --files setup.py')
        
    def test_too_many_args(self):
        '''Argument parser should die if given more than one positionnal argument'''
        self._assertSysExit(_args, '. sendcrap/')

    def test_invalid_dir(self):
        '''Argument parser should die if given an invalid directory'''
        self._assertSysExit(_args, 'setup.py')
    
    def test_invalid_file(self):
        '''Argument parser should die if given invalid file arguments'''
        self._assertSysExit(_args, '-f sendcrap/')
        
    def test_mutually_exclusive_opts(self):
        '''Argument parser should die if given both the verbose and quiet flags'''
        self._assertSysExit(_args, '-v -q')
        self._assertSysExit(_args, '-vq')
        self._assertSysExit(_args, '--verbose --quiet')
        self._assertSysExit(_args, '--verbose -q')
        self._assertSysExit(_args, '-v --quiet')
    
    def test_invalid_choices(self):
        '''Argument parser should die if given an unallowed option'''
        self._assertSysExit(_args, '-c doc')
        self._assertSysExit(_args, '-c bob doc')
        self._assertSysExit(_args, '-g family')
        self._assertSysExit(_args, '-g work family')
        self._assertSysExit(_args, '-g family -c doc')
    
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestArgParser))
    suite.addTest(unittest.makeSuite(TestArgParserInput))
    return suite
