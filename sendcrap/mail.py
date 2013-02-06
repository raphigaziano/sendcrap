#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
mail.py

Mail related features.

Author:  raphi <r.gaziano@gmail.com>
Created: 06/02/2013
Version: 1.0
"""
import conf

def get_template(tmpl):
    '''
    
    '''
    default  = conf.MAIL_TMPLS.get(conf.default_template, None)
    return conf.MAIL_TMPLS.get(tmpl, default)
    
    
def attach_or_upload(): pass # ??? in utils ?
def type_mail(): pass
def gen_mail(tmpl): pass # call get_template, interactive typing if needed, then gen actual mail data
def send_mail(*dummyargs): pass
