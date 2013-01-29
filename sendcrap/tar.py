#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
tar.py

BLAAA

Author:  raphi <r.gaziano@gmail.com>
Created: 24/01/2013
Version: 1.0
"""
import os
import tarfile
import conf
from . import utils

def get_size(*files): pass
def check_size(*files): pass

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
    # @TODO: check for size
    utils.output('Creating archive %s...' % tarname) 
    # Using mode 'w:gz' adds gzip compression, but nests
    # the tar inside the zip.
    with tarfile.open(tar_path, 'w') as tf:
        for f in files:
            utils.verbose_output("Adding %s to %s..." % (f, tarname))
            tf.add(f)
    return tar_path
