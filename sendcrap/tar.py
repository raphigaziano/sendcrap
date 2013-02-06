#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
tar.py

BLAAA

Author:  raphi <r.gaziano@gmail.com>
Created: 24/01/2013
Version: 1.0
"""
import sys
import os
import tarfile
import conf
from . import utils

__ALL__ = ['get_size', 'check_size', 'write']

def get_size(*files):
    '''Return the size in bytes of all the given files.'''
    size = 0
    for f in files:
        size += os.path.getsize(f)
    return size
    
def check_size(max_, *files):
    '''
    Return False if the given files' size exceeds the conf.SIZE_WARN
    constant.
    Will return true if conf.SIZE_WARN is set to None, causing all 
    checks to pass.
    '''
    if max_ is None: 
        return True
    s = get_size(*files)
    return True if s < max_ else False

def _size_warn():
    '''
    Prompt the user for cancellation.
    Returns True to go on, False to abort.
    '''
    # Py2/Py3 Compatibility
    if sys.version < '3':
        input = raw_input
        
    prompt = input('The given file list exceeds %s bytes.\n'
                   'Are you sure you want to upload that much data ? '
                   % conf.FILE_SIZE_WARN).lower()
    while True:
        if prompt.startswith('y'):
            return True
        elif prompt.startswith('n'):
            return False
        else:
            prompt = input('Please answer by y(es) or n(o) ').lower()
        

# @TODO: try using shutils.make_archive
def write(path, *files):
    '''
    Collects the given files into a single archive.
    Will issue a warning and eventually terminate if the overall files
    size considered too great (according to the conf.SIZE_WARN 
    constant).
    
    @param path:  The path of root directory. Archive will be created 
                  there and named after it.
    @param files: Pathes of all the files to be collected, provided as
                  a variable number of strings.
    @return:      Path to the created archive.
    '''
    dirname = os.path.basename(path)
    tarname = '%s.tar' % dirname
    tar_path = os.path.join(path, tarname)
    # Warn user if file size is considered too big
    if not check_size(conf.FILE_SIZE_WARN, *files) and not _size_warn():
        utils.forced_output('Aborting')
        sys.exit(0)
    utils.output('Creating archive %s...' % tarname) 
    # Using mode 'w:gz' adds gzip compression, but nests
    # the tar inside the zip.
    with tarfile.open(tar_path, 'w') as tf:
        for f in files:
            utils.verbose_output("Adding %s to %s..." % (f, tarname))
            tf.add(f)
    return tar_path
