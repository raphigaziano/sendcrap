#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
Recipients test file.
Test the retrieving of a recipients list.
"""
import unittest
from sendcrap.utils import get_recipients

# Replacing utils conf with the dummy sample config file
from sendcrap import utils
import conf_sample as conf
utils.conf = conf

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
        '''get_recipients([grp]) should return the requested group's adresses as a list'''
        for grp, c_list in conf.GROUPS.items():
            expected = [conf.ADRESSES[c] for c in c_list]
            self._check_recipients(expected, get_recipients([grp]))
    
    def test_get_multiple_groups(self):
        '''get_recipients([...]) should return all the requested groups' adresses as a list'''
        inp = []
        expected = []
        for grp, c_list in conf.GROUPS.items():
            inp.append(grp)
            expected += [conf.ADRESSES[c] for c in c_list]
        expected = list(set(expected))
        self._check_recipients(expected, get_recipients(inp))

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

    def test_get_group_plus_contacts(self):
        '''get_recipients(grps=[...], contacts=[...]'''
        expected = [conf.ADRESSES[c] for c in conf.GROUPS['pals']]
        grp_args = expected[:]
        c_args = ['blondie']
        for c in c_args: expected.append(conf.ADRESSES[c])
        self._check_recipients(expected, get_recipients(grps=['pals'],
                                                        contacts=c_args))
        
    def test_get_group_plus_arbitrary(self):
        '''get_recipients(grps=[...], arbs=[...]'''
        expected = [conf.ADRESSES[c] for c in conf.GROUPS['work']]
        arb_args = ['test@unit.woo', 'captain.wienner@dom.co']
        expected += arb_args
        self._check_recipients(expected, get_recipients(grps=['work'],
                                                        arbs=arb_args))
                                                                
    def test_get_contacts_plus_arbitrary(self):
        '''get_recipients(contacts=[...], arbs=[...]'''
        c_args = ['marylou', 'vader', 'blondie']
        arb_args = ['test@unit.woo', 'captain.wienner@dom.co']
        expected = [conf.ADRESSES['marylou'], conf.ADRESSES['vader'], 
                    conf.ADRESSES['blondie']
        ]
        expected += arb_args
        self._check_recipients(expected, get_recipients(contacts=c_args,
                                                        arbs=arb_args))
        
    def test_get_all_opts(self):
        '''get_recipients(grups=[...], contacts=[...], arbs=[...])'''
        grp_args = ['work']
        expected = [conf.ADRESSES[c] for c in conf.GROUPS['work']]
        c_args = ['vader']
        expected += [conf.ADRESSES[c] for c in c_args]
        arb_args = ['test@unit.woo', 'captain.wienner@dom.co']
        expected += arb_args
        self._check_recipients(expected, get_recipients(grps=grp_args,
                                                        contacts=c_args,
                                                        arbs=arb_args))
                                                        
    def test_no_duplicates(self):
        '''get_recipients() should return no duplicates'''
        expected = ['test@test.net']
        self._check_recipients(expected, 
                               get_recipients(arbs=['test@test.net',
                                                    'test@test.net',
                                                    'test@test.net'])
        )
        expected = ['bob@bob.com']
        self._check_recipients(expected, 
                               get_recipients(contacts=['bob', 'bob',
                                                        'bob', 'bob'])
        )
        
    # bad input
    
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestRecipients))
    return suite
