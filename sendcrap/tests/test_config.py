#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
Configuration test file.
Test config import and reading.

Hmm... Most of those tests are testing python dicts rather than 
anything else...
"""
import unittest
import imp, importlib
import conf_sample as conf

class TestConfig(unittest.TestCase):
    '''Config file Tests'''
    def setUp(self): 
        pass
        
    def tearDown(self):
        '''
        Reload conf module to ensure its back to its original state
        for each test
        '''
        imp.reload(conf)
    
    def test_read_conf(self):
        '''Retrieving data from the config file'''
        self.assertEqual("bob@bob.com", conf.CONTACTS.get('bob'))
        self.assertTrue('marylou' in conf.CONTACTS)
        
    def test_write_conf(self):
        '''Writing to conf file (for dynamic conf overriding)'''
        conf.CONTACTS['bob'] = 'new@mail.woot'
        self.assertEqual('new@mail.woot', conf.CONTACTS.get('bob'))

    def test_nondefined_opts(self):
        '''Directly accessing non defined conf opts should raise a KeyError Exception.'''
        self.assertRaises(KeyError, lambda: conf.CONTACTS['poil'])

    def test_get_nondefined_opts(self):
        '''Accessing non defined conf opts with get method return None of def value'''
        self.assertEqual(None, conf.CONTACTS.get('poil'))
        self.assertEqual('foo', conf.CONTACTS.get('poil', 'foo'))
        
    def test_stoopid_indexing(self):
        '''Getting conf opts using another conf opt'''
        self.assertEqual('bob@bob.com', 
                         conf.CONTACTS[conf.GROUPS['pals'][0]]
        )
        
    def test_import_uploader(self):
        '''Importing uploader module specified in conf'''
        mod = None
        import_string = 'sendcrap.uploaders.%s' % conf.UPLOADER
        try:
            mod = importlib.import_module(import_string)
        except ImportError:
            self.fail('Unable to import %s module' % conf.UPLOADER)
        self.assertEqual(str(type(mod)), "<type 'module'>")
        
    def test_invalid_uploader(self):
        '''Trying to import a non existent uploader module should fail'''
        conf.UPLOADER = "randomcrap"
        import_string = 'sendcrap.uploaders.%s' % conf.UPLOADER
        self.assertRaises(ImportError, 
                          importlib.import_module,
                          import_string)        

    # This is testing configuration sanity rather than actual code...
    def test_groups_vals(self):
        '''All names in a group should be defined in the ADRESSES dict constant.'''
        for group, c_list in conf.GROUPS.items():
            for contact in c_list:
                self.assertTrue(contact in conf.CONTACTS)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestConfig))
    return suite
