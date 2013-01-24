#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
optparser.py

Definition of an argparse parser.
This is the parser that will be used by default - We'll fall back to
using optparser if the local python installation cannot handle this one.

Author:  raphi <r.gaziano@gmail.com>
Created: 21/01/2013
Version: 1.0
"""
import os
import argparse
import conf

### Args Checkers ###
#####################

# @TODO: move in _common module ?
# Adapted from:
# http://stackoverflow.com/questions/11415570/directory-path-types-with-argparse

class _CheckPathArg(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if not isinstance(values, list): pathes = [values]
        else: pathes = values
        for p in pathes:
            if not self.check_func(p):
                raise argparse.ArgumentError(self,
                    "%s is not a valid %s" % (p, self.type_))
            if os.access(p, os.R_OK):
                setattr(namespace, self.dest, values)
            else:
                raise argparse.ArgumentError(self,
                    "%s is not a readable %s" % (p, self.type_))

class IsDir(_CheckPathArg):
    type_ = 'directory'
    def check_func(self, p):
        if p is None: return False
        return os.path.isdir(p)
            
class IsFile(_CheckPathArg):
    type_ = 'file'
    def check_func(self, p): 
        return os.path.isfile(p)


class CleanExt(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        exts = [".%s" % e 
                if not e.startswith('.') else e 
                for e in values]
        setattr(namespace, self.dest, exts)

### Parser Definition ###
#########################

#-- @TODO: Documentation strings should be defined elsewhere for easier
#-- editing/reuse.
doc_header = \
'''Man i should write some doc
someday.
blabla lala toussa.
'''
doc_footer = \
'''Wouhou, footer doc
'''

parser = argparse.ArgumentParser(description=doc_header, 
                                 epilog=doc_footer)

#-- flags
flags = parser.add_argument_group('flags')
verbosity_grp = flags.add_mutually_exclusive_group()
verbosity_grp.add_argument('-v', '--verbose', action='store_true')
verbosity_grp.add_argument('-q', '--quiet', action='store_true')
h = 'search directories recursively'
flags.add_argument('-r', '--recursive', action='store_true', help=h)
h = ('dummy run: show what will be sent and to whom, but don\'t'
     ' actually do anything')
flags.add_argument('-d', '--dummy', action='store_true', help=h)
h = '???'
flags.add_argument('-F', '--FFF', action='store_true', help=h)

#-- files
h = ('Select files to pack up and upload.\nIf none of these options are'
     ' provided, then the selection will default to the contents of the'
     ' current working directory.')
f_opts = parser.add_argument_group('file selection', description=h)
h = 'Target directory. dir\'s contents will be archived as dir/dir.tar.'
f_opts.add_argument('dir', metavar='dir', nargs='?', default='.',
                    action=IsDir, help=h)
h = 'List of arbitrary files to add to the selection.'
f_opts.add_argument('-f', '--files', metavar='F', nargs='*', default=[],
                    action=IsFile, help=h)
h = ('Filter selection based on the provided list of file extensions.\n'
     'Extensions can be provided with or without a leading dot '
     '(Eg both ".txt" & "txt" will work).')
f_opts.add_argument('-e', '--exts', metavar='EXT', nargs='*',
                    default=[], action=CleanExt, help=h)
                    
#-- mail
h = ('Select recipients to notify of the file upload.')
m_opts = parser.add_argument_group('contact selection', description=h)
h = ('Adds all members of the given contact groups to the list of '
     'recipients.\nGRP must be defined in the configuration file')
m_opts.add_argument('-g', '--groups', metavar='GRP', nargs='*',
                    default=[], choices=[g for g in conf.GROUPS.keys()],
                    help=h)
h = ('Adds the given contacts to the list of recipients.\nCONT must be '
     'defined in the configuration file.')
m_opts.add_argument('-c', '--contacts', metavar='CONT', nargs='*',
                    default=[], choices=[c for c in conf.CONTACTS.keys()],
                    help=h)
h = ('Adds the given list of arbitrary mail addresses to the list of \n'
     'recipients.')
m_opts.add_argument('-a', '--addr', metavar='ADD', nargs='*',
                    default=[], help=h)
# mail template (but later...)

