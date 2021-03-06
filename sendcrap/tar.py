#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
tar.py

tar archive builder.

Author:  raphi <r.gaziano@gmail.com>
Created: 24/01/2013
Version: 1.0
"""
import sys
import os
import tarfile
from . import conf, utils

__ALL__ = ['write']
        
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
    dirname = os.path.basename(os.path.abspath(path))
    tarname = '%s.tar' % dirname
    tar_path = os.path.join(path, tarname)
    # Warn user if file size is considered too big
    if not utils.check_size_warn(conf.FILE_SIZE_WARN, *files):
        utils.forced_output('Aborting')
        sys.exit(0)
    utils.output('Creating archive %s...' % tarname) 
    # Using mode 'w:gz' adds gzip compression, but nests
    # the tar inside the zip.
    with tarfile.open(tar_path, 'w') as tf:
        for f in files:
            path = os.path.relpath(f)
            utils.verbose_output("Adding %s to %s..." % (path, tarname))
            try:
                tf.add(path)
            # ???
            # If given a single list for *files, windows will raise
            # a TypeError, while linux will raise an AttributeError ???
            # Quickfix: Simply catch AttributeError and raise TypeError
            # Instead.
            except AttributeError as e: raise TypeError(str(e))
    return tar_path
