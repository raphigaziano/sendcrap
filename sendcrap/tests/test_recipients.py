#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
Recipients test file.
Test the retrieving of a recipients list.
"""
import unittest
from sendcrap.utils import get_recipients
import conf

class TestRecipients(unittest.TestCase):
    '''Recipient retrieval Tests'''
    def setUp(self): pass
    def tearDown(self): pass
    
    def _check_recipients(self, expected, received):
        '''Common helper for the individual tests''' 
        self.assertTrue(all([e in received for e in expected]))
        self.assertTrue(all([r in expected for r in received]))
    
    def test_no_input(self):
        '''get_recipients() (No args) should return an empty list'''
        self.assertEqual([], get_recipients())
        
    def test_get_group(self):
        '''get_recipients(grp) should return the requested group's adresses as a list'''
        for grp, c_list in conf.GROUPS.items():
            expected = [conf.ADRESSES[c] for c in c_list]
            self._check_recipients(expected, get_recipients(grp))
            
    def test_get_contacts(self):
        '''get_recipients(contacts=[...]) should return the requested contacts' adresses'''
        contacts = conf.ADRESSES.keys()
        expected = conf.ADRESSES.values()
        self._check_recipients(expected, 
                               get_recipients(contacts=contacts))
        contacts = contacts[:1] + contacts[-1:]
        expected = expected[:1] + expected[-1:]
        self._check_recipients(expected, 
                               get_recipients(contacts=contacts))
                               
    def test_get_arbs(self):
        '''get_recipients(arbs=[...]) should return only the provided mail adresses'''
        expected = [
            'dummy@dumdum.net',
            'greenturnip@rattleboobies.com',
            'listless.porpoise@zogzog.org'
        ]
        self._check_recipients(expected, get_recipients(arbs=expected))

    # grp + contacts
    # grp + arbs
    # contacts + arbs
    # all


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestRecipients))
    return suite
