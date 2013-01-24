#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
args.py

Command line arguments parsing.
This will fail with python versions < 2.7, until an optparse 
implementation of the argument parser is provided OR the backported
argparse module is installed.

Author:  raphi <r.gaziano@gmail.com>
Created: 19/01/2013
Version: 1.0
"""
import os
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

try:
    from .argparsers.argparser import parser as _parser
except ImportError:
    from .argparsers.optparser import parser as _parser
    
def parse_args():
    '''
    DOC
    '''
    return _parser.parse_args()
    
# This only support the argparse parser.
# If optparse support is to be added, then 2 different versions of 
# process_args should be defined along with the parsers and imported
# here.
# This one should simply be cut and pasted into argparsers.argparser,
# leaving arpasers.optparser.process_args to be defined.
def process_args(args=None):
    '''DOC
    
    @param args: Namespace or WHETAVAR __CLASS__ obj returned by parser.
    '''
    # Error checking: no real work has begun yet, so simply die rather 
    # than throw exception.
    ''' or, better(?):
    ArgumentParser.exit(status=0, message=None)
    This method terminates the program, exiting with the specified 
    status and, if given, it prints a message before that.

    ArgumentParser.error(message)
    This method prints a usage message including the message to the 
    standard error and terminates the program with a status code of 2.
    '''
    if args is None: args = parse_args()
    files, mails = [], []
    import pprint
    #~ pprint.pprint(_list_files(args.dir, args.recursive,
                              #~ args.exts, args.files))
    
    return files, mails
