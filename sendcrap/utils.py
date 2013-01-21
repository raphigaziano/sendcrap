#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
utils.py

Various utilities.

Author:  raphi <r.gaziano@gmail.com>
Created: 19/01/2013
Version: 1.0
"""
import os
import conf
    
def list_files(dir_=None, walk=False, exts=None, arbs=None):
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
                    if exts and not f.endswith(*exts): continue
                    all_files.append(os.path.join(root, f))
        else:
            for f in os.listdir(dir_):
                if exts and not f.endswith(*exts): continue
                p = os.path.join(dir_, f)
                if os.path.isfile(p):
                    all_files.append(p)
    # Add arbitrary files
    for f in arbs:
        all_files.append(f)
        
    return all_files

def get_recipients(grps=None, contacts=None, arbs=None):
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
            all_recs.append(conf.ADRESSES[contact])
    for contact in contacts:
        all_recs.append(conf.ADRESSES[contact])
    for a in arbs:
        all_recs.append(a)
    
    # Remove any duplicate
    all_recs = list(set(all_recs))
    return all_recs
    
