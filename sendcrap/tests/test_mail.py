#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
Mail test file.
Test the mail generation and sending features.
"""
import sys
import unittest
from sendcrap.mail import get_template

# Replacing mail conf with the dummy sample config file
from sendcrap import mail
import conf_sample as conf
mail.conf = conf

class TestTemplates(unittest.TestCase):
    '''Template retrieval Tests'''
    def setUp(self): pass
    def tearDown(self): pass
    
    def test_get_template(self):
        '''mail.get_template should return the right template'''
        for t in conf.MAIL_TMPLS.keys():
            self.assertEqual(get_template(t), conf.MAIL_TMPLS[t])
            
    def test_get_default_template(self):
        '''mail.get_template should return the default template if one is set and no input ovverrides it'''
        conf.default_template = 'tongs'
        self.assertEqual(get_template(None), conf.MAIL_TMPLS['tongs'])
        conf.default_template = None
        
    def test_no_template(self):
        '''mail.get_template should return None if no args and no default'''
        from sendcrap.mail import type_mail as base_type_mail
        mail.type_mail = lambda: 'dummytyping'
        self.assertEqual(get_template(None), 'dummytyping')
        mail.type_mail = base_type_mail
    
    
if sys.version < '3':
    try:
        from StringIO import StringIO
    except ImportError:
        from cStringIO import StringIO
else:
    try:
        from io import StringIO
    except ImportError:
        from io import cStringIO as StringIO

from sendcrap.mail import type_mail
    
class TestTypeMail(unittest.TestCase):
    '''Interactive mail typing tests'''
    def setUp(self):
        sys.stdin = StringIO()
        
    def tearDown(self):
        sys.stdin = sys.__stdin__
    
    def _set_up_stdin(self, *lines):
        '''Quick helper'''
        for l in lines:
            sys.stdin.write(l)
        sys.stdin.seek(0)
    
    def test_no_header(self):
        '''mail.type_mail should return None if no header is given'''
        self._set_up_stdin('\n')
        self.assertEqual(type_mail(), None)
    
    def test_header_to_tmpl(self):
        '''mail.type_mail should return the given template if a template name is given as the mail header'''
        for t in conf.MAIL_TMPLS.keys():
            self._set_up_stdin('%s\n' % t)
            self.assertEqual(type_mail(), conf.MAIL_TMPLS[t])
            # Cannot use StringIO.truncate method for py3 compatibility
            sys.stdin = StringIO()
            
    def test_body(self):
        '''mail.type_mail should return a well formed dict when given valid input'''
        expected = {'header': 'testtest', 'body': 'pimpampoom'}
        vals = [
            '%s\n' % expected['header'], 
            '%s\n' % expected['body']
        ]
        self._set_up_stdin(*vals)
        self.assertEqual(type_mail(), expected)
        
    def test_body_with_endlines(self):
        '''mail.type_mail should ignore explicit line feeds'''
        expected = {'header': 'testtest', 'body': 'pimpampoom\\npampampam'}
        vals = [
            '%s\n' % expected['header'], 
            '%s\n' % expected['body']
        ]
        self._set_up_stdin(*vals)
        self.assertEqual(type_mail(), expected)
    
    
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestTemplates))
    suite.addTest(unittest.makeSuite(TestTypeMail))
    return suite
