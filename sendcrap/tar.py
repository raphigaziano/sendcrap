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
    '''DOC'''
    dirname = os.path.basename(path)
    tarname = dirname + '.tar'
    # Using mode 'w:gz' adds gzip compression, but nests
    # the tar inside the zip.
    utils.output('Creating archive %s...' % tarname) 
    with tarfile.open(os.path.join(path, tarname), 'w') as tf:
        for f in files:
            utils.verbose_output("Adding %s to %s..." % (f, tarname))
            tf.add(f)
    return tf
