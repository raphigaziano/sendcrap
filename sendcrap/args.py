#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
args.py

Command line arguments parsing.
This will fail with python versions < 2.7, unless the backported 
argparse module is installed.

Author:  raphi <r.gaziano@gmail.com>
Created: 19/01/2013
Version: 1.0
"""
import os
import argparse
import conf

__ALL__ = ['parse_args', 'process_args']
    
### Helpers ###
###############
    
def _list_files(dir_=None, walk=False, exts=None, arbs=None):
    '''
    Return a list of all the files meeting the provided criterias.
    
    @param dir_: Optional. Search directory.
    @param walk: Boolean indicating if subdirectories should be 
                 searched. Defaults to False.
    @param exts: Optional. List of valid file extensions
    @param arbs: Optional. List of arbitrary files to be included.
                 Those files will be added to the selection no 
                 matter what.
    @returns:    List of relative paths to all valid files.
    '''
    if exts is None: exts = []
    if arbs is None: arbs = []
    all_files = []
    if dir_ is not None:
        if walk:
            for root, dirs, files in os.walk(dir_):
                for f in files:
                    all_files.append(os.path.join(root, f))
        else:
            for f in os.listdir(dir_):
                p = os.path.join(dir_, f)
                if os.path.isfile(p):
                    all_files.append(p)
    # Filter by extension
    if exts:
        all_files = [f  for f in all_files 
                     if os.path.splitext(f)[1] in exts]
    # Add arbitrary files
    for f in arbs:
        all_files.append(f)
        
    return all_files

def _get_recipients(grps=None, contacts=None, arbs=None):
    '''
    Return a list of contacts according to the provided args.
    
    @param grps:     Optional. List of requested contact groups.
    @param contacts: Optional. List of requested contacts indexed in the 
                     config file. 
    @param arbs:     Optional. List of arbitrary mail adresses to be
                     added to the selection.
    @returns:        List of contact adresses, with no duplicates.
    '''
    if grps is None: grps = []
    if contacts is None: contacts = []
    if arbs is None: arbs = []
    all_recs = []
    for grp in grps:
        for contact in conf.GROUPS.get(grp, []):
            all_recs.append(conf.CONTACTS[contact])
    for contact in contacts:
        all_recs.append(conf.CONTACTS[contact])
    for a in arbs:
        all_recs.append(a)
    # Remove any duplicate
    all_recs = list(set(all_recs))
    return all_recs


### Args Processing ###
#######################

### Args Checkers ###

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

_parser = argparse.ArgumentParser(description=doc_header, 
                                 epilog=doc_footer)

#-- flags
flags = _parser.add_argument_group('flags')
verbosity_grp = flags.add_mutually_exclusive_group()
verbosity_grp.add_argument('-v', '--verbose', action='store_true')
verbosity_grp.add_argument('-q', '--quiet', action='store_true')
h = 'search directories recursively'
flags.add_argument('-r', '--recursive', action='store_true', help=h)
h = ('dummy run: show what will be sent and to whom, but don\'t'
     ' actually do anything')
flags.add_argument('-d', '--dummy', action='store_true', help=h)

#-- files
h = ('Select files to pack up and upload.\nIf none of these options are'
     ' provided, then the selection will default to the contents of the'
     ' current working directory.')
f_opts = _parser.add_argument_group('file selection', description=h)
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
                    
#-- contacts
h = ('Select recipients to notify of the file upload.')
c_opts = _parser.add_argument_group('contact selection', description=h)
h = ('Adds all members of the given contact groups to the list of '
     'recipients.\nGRP must be defined in the configuration file')
c_opts.add_argument('-g', '--groups', metavar='GRP', nargs='*',
                    default=[], choices=[g for g in conf.GROUPS.keys()],
                    help=h)
h = ('Adds the given contacts to the list of recipients.\nCONT must be '
     'defined in the configuration file.')
c_opts.add_argument('-c', '--contacts', metavar='CONT', nargs='*',
                    default=[], choices=[c for c in conf.CONTACTS.keys()],
                    help=h)
h = ('Adds the given list of arbitrary mail addresses to the list of \n'
     'recipients.')
c_opts.add_argument('-a', '--addr', metavar='ADD', nargs='*',
                    default=[], help=h)
h = ('Use the given mail template. Will default to the value defined in '
     'the configuration file')

#-- mail
m_opts = _parser.add_argument_group('mail options')
m_opts.add_argument('-t', '--template', default=conf.default_template,
                    choices = [t for t in conf.MAIL_TMPLS.keys()],
                    metavar='template', help=h)

### Actual Arg proccessing ###
    
def parse_args():
    '''Convenience wrapper around the parser parse_args method.'''
    return _parser.parse_args()
    
def process_args(args=None):
    '''
    Process the program's command line arguments and sets up all 
    options. 
    Side effect: the configuration file's flag variables will be modified
    here.
    
    @param args: Optional. Namespace object returned by the argument 
                 parser.
    @returns:    The list of files to pack and upload, and the list of
                 contacts to notify. Either list can be empty.
    '''
    # Invalid arguments are handled by the parser itself.
    if args is None: args = parse_args()
    # Flags
    conf.verbose   = args.verbose
    conf.quiet     = args.quiet
    conf.recursive = args.recursive
    conf.dummy     = args.dummy
    
    files = _list_files(args.dir, args.recursive, args.exts, args.files)
    mails = _get_recipients(args.groups, args.contacts, args.addr)
    
    return files, mails
    
