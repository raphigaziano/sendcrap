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
from . import utils

def get_template(tmpl):
    '''
    Return the required template from the ones defined in the 
    configuration file.
    
    @param tmpl: Requested template's name. If none, will either return
                 the default template if one is defined, or call 
                 type_mail() to allow the user to type his mail.
    @returns:    Dict template {header, body}. 
    '''
    default  = conf.MAIL_TMPLS.get(conf.default_template, None)
    return conf.MAIL_TMPLS.get(tmpl, default) or type_mail()

def type_mail(_print_header_help=True): 
    '''
    Prompt the user to type its mail interactively.
    When asked for the header, several special cases might occur:
    - User enters nothing: function returns immediatly and no mail will
      be sent
    - user enters a registered template name: use the requested 
      template.
    - user enters "list": list all available templates from the config
      file, then call self recursively.
    
    @returns: A template like dict (see get_template) containing the
              typed mail header and body, or None if user has cancelled.
    '''
    # @TODO: actual help msgs
    if _print_header_help: 
        utils.forced_output('help aboot entering nonthing or tmplname...')
    header = utils.input('header: ')
    # Special cases
    if header == '':
        return None
    elif header == 'list':
        utils.forced_output("Available templates:\n\t%s" %
            "\n\t".join(t for t in conf.MAIL_TMPLS.keys()))
        return type_mail(_print_header_help=False)
    elif header in conf.MAIL_TMPLS.keys(): 
        return conf.MAIL_TMPLS[header]
    
    utils.forced_output('quick help aboot body (explicit \\n!)')
    body = []
    while True:
        if not body: prompt = 'body: '
        else:        prompt = ' >>>  '
        line = utils.input(prompt)
        body.append(line)
        if not line: break
    return {'header': header, 'body': "\n".join(body)}
    
def gen_mail(tmpl): pass 
def send_mail(*dummyargs): pass
