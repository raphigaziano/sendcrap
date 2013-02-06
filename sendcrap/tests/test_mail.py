#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
Mail test file.
Test the mail generation and sending features.
"""
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
        self.assertEqual(get_template(None), None)
    
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestTemplates))
    return suite
