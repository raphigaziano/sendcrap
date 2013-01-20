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
    
def list_files(dir_=None, walk=False, exts=None, arb_files=None):
    '''
    Return a list of all the files meeting the provided criterias.
    
    @param dir_:      Optional. Search directory.
    @param walk:      Boolean indicating if subdirectories should be 
                      searched. Defaults to False.
    @param exts:      Optional. List of valid file extensions
    @param arb_files: Optional. List of arbitrary files to be included.
                      Those files will be added to the selection no 
                      matter what.
    @returns:         List of relative paths to all valid files.
    '''
    if exts is None: exts = []
    if arb_files is None: arb_files = []
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
    for f in arb_files:
        all_files.append(f)
        
    return all_files

