#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
mail.py

Mail related features.

Author:  raphi <r.gaziano@gmail.com>
Created: 06/02/2013
Version: 1.0
"""
import smtplib
import os
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders
import getpass

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
    
    utils.forced_output('quick help aboot body (empty line to stop!)')
    body = []
    while True:
        if not body: prompt = 'body: '
        else:        prompt = ' >>>  '
        line = utils.input(prompt)
        body.append(line)
        if not line: break
    return {'header': header, 'body': "\n".join(body)}
    
def gen_mail(tmpl): pass 

def send_mail(tmpl, recipients, file_ ):
    # TESTTESTTEST ###
    # inspired:
    # http://www.dzone.com/snippets/send-email-attachments-python
    assert type(recipients) == list

    msg = MIMEMultipart()
    msg['From'] = 'r.gaziano@gmail.com'
    msg['To'] = COMMASPACE.join(recipients)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = tmpl['header']

    msg.attach( MIMEText(tmpl['body']) )

    part = MIMEBase('application', 'octet-stream')
    part.set_payload(open(file_, 'rb').read())
    Encoders.encode_base64(part)
    part.add_header('Content-Disposition',
           'attachment; filename="%s"' % os.path.basename(file_))
    msg.attach(part)

    smtp = smtplib.SMTP(conf.SMTP_SERVR, conf.SMTP_PORT)
    # Try and send mail directly, in case the server doesn't require
    # authentiication (is that even possible?)
    #~ try:
        #~ res = smtp.sendmail(conf.SENDER_EMAIL, recipients, 
                            #~ msg.as_string())
    #~ except smtplib.SMTPAuthenticationError:
    smtp.starttls()
    smtp.ehlo()
    login = conf.MAIL_LOGIN or utils.input("mail login: ")
    pswd  = conf.MAIL_PSWRD or getpass.getpass("mail pswd: ")
    smtp.login(login, pswd)
    res = smtp.sendmail(conf.SENDER_EMAIL, recipients, 
                        msg.as_string())
    smtp.close()
    # res contains 
    # "a dictionary, with one entry for each recipient that was refused. 
    # Each entry contains a tuple of the SMTP error code and the 
    # accompanying error message sent by the server."
    print(res)
