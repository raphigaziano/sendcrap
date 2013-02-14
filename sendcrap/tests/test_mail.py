#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
Mail test file.
Test the mail generation and sending features.
"""
import os, sys
import unittest
from sendcrap.mail import get_template, gen_mail

# Replacing mail conf with the dummy sample config file
from sendcrap import mail
import conf_sample as conf
mail.conf = conf

URL  = 'http://www.python.org'
PATH = __file__
HTML_URL = mail.HTML_URL_TMPL % (URL, URL)

TMPL_BASE  = {"header": "testemail"}
RECIPIENTS = ['test@test.com', 'another@test.com']

def gen_template(body):
    '''Helper. Generate a template with the passed body text'''
    tmpl = TMPL_BASE
    tmpl['body'] = body
    return tmpl
    
# from:
# http://stackoverflow.com/questions/7519964/python-pull-back-plain-text-body-from-message-from-imap-account
def get_mail_plain_body(message):
    '''Helper. Extract the body from a Message objet'''
    for part in message.walk():       
        if part.get_content_type() == "text/plain":
            try:
                return str(part.get_payload(decode=True), 'utf8')
            except TypeError:
                return part.get_payload(decode=True)

def get_mail_html_body(message):
    '''Helper. Extract the html body from a Message objet'''
    for part in message.walk():       
        if part.get_content_type() == "text/html":
            try:
                return str(part.get_payload(decode=True), 'utf8')
            except TypeError:
                return part.get_payload(decode=True)

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
    
    # Email generation #

    def test_recipients(self):
        '''mail.gen_mail should return a Message object with the right recipient list'''
        m = gen_mail(gen_template('dummy'), RECIPIENTS, PATH)
        self.assertEqual(m['To'], ", ".join(RECIPIENTS))
        # single recipient
        m = gen_mail(gen_template('dummy'), ['bob@bob.com'], PATH)
        self.assertEqual(m['To'], 'bob@bob.com')
        
    def test_sender(self):
        '''mail.gen_mail should return a Message object with the right From field (depending on conf)'''
        m = gen_mail(gen_template('dummy'), RECIPIENTS, PATH)
        self.assertEqual(m['From'], conf.SENDER_EMAIL)
        
    def test_subject(self):
        '''mail.gen_mail should set the right subject (from chosen template)'''
        t = gen_template('dumdummy')
        m = gen_mail(t, RECIPIENTS, PATH)
        self.assertEqual(m['Subject'], t['header'])
        
    # Template processing #
    
    def test_templ_no_tag_local_file(self):
        '''mail.gen_mail with local file => template not containing any url tag'''
        tmpl = gen_template('testtesttesttest')
        m = gen_mail(tmpl, RECIPIENTS, PATH)
        self.assertEqual(get_mail_plain_body(m), 'testtesttesttest')

    def test_templ_tag_local_file(self):
        '''mail.gen_mail with local file => template containing url tag to be stripped'''
        tmpl = gen_template('testtest%stest')
        m = gen_mail(tmpl, RECIPIENTS, PATH)
        self.assertEqual(get_mail_plain_body(m), 'testtesttest')
        tmpl = gen_template('testtest\n%s\ntest')
        m = gen_mail(tmpl, RECIPIENTS, PATH)
        self.assertEqual(get_mail_plain_body(m), 'testtesttest')
        tmpl = gen_template('testtest%s\ntest')
        m = gen_mail(tmpl, RECIPIENTS, PATH)
        self.assertEqual(get_mail_plain_body(m), 'testtesttest')
        tmpl = gen_template('testtest\n%stest')
        m = gen_mail(tmpl, RECIPIENTS, PATH)
        self.assertEqual(get_mail_plain_body(m), 'testtesttest')

    def test_templ_no_tag_remote_file(self):
        '''mail.gen_mail with url => no url tag '''
        tmpl = gen_template('testtesttest')
        m = gen_mail(tmpl, RECIPIENTS, URL)
        self.assertEqual(get_mail_plain_body(m), 'testtesttest\n%s' % URL)
        self.assertEqual(get_mail_html_body(m), 'testtesttest\n%s' % HTML_URL)
    
    def test_templ_tag_remote_file(self):
        '''mail.gen_mail with url => with url tag '''
        tmpl = gen_template('testtest%stest')
        m = gen_mail(tmpl, RECIPIENTS, URL)
        self.assertEqual(get_mail_plain_body(m), 'testtest%stest' % URL)
        self.assertEqual(get_mail_html_body(m), 'testtest%stest' % HTML_URL)
    
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
        expected = {'header': 'testtest', 'body': 'pimpampoom\n'}
        vals = [
            '%s\n' % expected['header'], 
            '%s\n' % expected['body']
        ]
        self._set_up_stdin(*vals)
        self.assertEqual(type_mail(), expected)
        
    def test_body_with_endlines(self):
        '''mail.type_mail should ignore explicit line feeds'''
        expected = {'header': 'testtest', 'body': 'pimpampoom\npampampam\n'}
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
