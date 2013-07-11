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
import imp
from docopt import DocoptExit
from sendcrap.args import parse_args, process_args
# Replacing args conf with the dummy sample config file
from sendcrap import args
import conf_sample as conf
args.conf = conf

def _args(args):
    '''Common helper for the individual tests - parse the given args'''
    return parse_args(args.split())

def _pargs(args):
    '''Common helper for the individual tests - process the given args'''
    return process_args(_args(args))

# A lot of the process_args functionnality comes from its use of
# args._list_files & args._get_recipients and won't be tested here.
# See test_file_list.py & test_recipients.py for tests related to these
# two functions.
class TestArgParser(unittest.TestCase):
    '''Command line processing tests'''
    def tearDown(self): 
        self.flist = []
        self.mlist = []
        imp.reload(conf)
        
    def _p(self, args):
        self.flist, self.mlist = _pargs(args)
    
    #~ def test_no_input(self): self.fail()
    #~ def test_no_file_input(self): self.fail()
    
    def test_no_mail_input(self):
        '''process_args should return an empty mail list if not given any contact opts'''
        for args in ('', 'sendcrap/', '-e txt', '-r'):
            self._p(args)
            self.assertTrue(len(self.mlist) == 0)
    
    def test_mlist_len_grps(self):
        '''process_args should return the right number of mail adresses for a given group'''
        for grp in conf.GROUPS:
            self._p('-g %s' % grp)
            self.assertTrue(len(self.mlist) == len(conf.GROUPS[grp]))

    def test_mlist_len_contacts(self):
        '''process_args should return the right number of mail adresses for a given set of contacts'''
        self._p('-c ' + ' -c '.join([c for c in conf.CONTACTS]))
        self.assertTrue(len(self.mlist) == len(conf.CONTACTS))

    # flags setting
    def test_flag_v(self):
        '''process_args should set the verbose flag if opt is provided'''
        self._p('-v')
        self.assertTrue(conf.verbose)
        
    def test_flag_q(self):
        '''process_args should set the quiet flag if opt is provided'''
        self._p('-q')
        self.assertTrue(conf.quiet)
        
    def test_flag_r(self):
        '''process_args should set the recursive flag if opt is provided'''
        self._p('-r')
        self.assertTrue(conf.recursive)
        
    def test_flag_d(self):
        '''process_args should set the dummy flag if opt is provided'''
        self._p('-d')
        self.assertTrue(conf.dummy)


class TestArgParserInput(unittest.TestCase):
    '''Error handling related to received arguments'''
    def setUp(self):
        self.buffer_ = StringIO()

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
        self.assertRaises(DocoptExit, _args, '-o')
        self.assertRaises(DocoptExit, _args, '-xjk')
        self.assertRaises(DocoptExit, _args, '-o -g -t')
        # Non existent along with correct flags:
        self.assertRaises(DocoptExit, _args, '-ro')
        self.assertRaises(DocoptExit, _args, '-r -o')

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
        self.assertRaises(DocoptExit, _args, '-c doc')
        self.assertRaises(DocoptExit, _args, '-c bob doc')
        self.assertRaises(DocoptExit, _args, '-g family')
        self.assertRaises(DocoptExit, _args, '-g work family')
        self.assertRaises(DocoptExit, _args, '-g family -c doc')
    
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestArgParser))
    suite.addTest(unittest.makeSuite(TestArgParserInput))
    return suite
