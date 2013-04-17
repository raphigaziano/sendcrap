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
import re
import getpass
try: # py2
    from email.MIMEMultipart import MIMEMultipart
    from email.MIMEBase import MIMEBase
    from email.MIMEText import MIMEText
    from email.Utils import COMMASPACE, formatdate
    from email import Encoders
except ImportError: #py3
    from email.mime.multipart import MIMEMultipart
    from email.mime.base import MIMEBase
    from email.mime.text import MIMEText
    from email.utils import COMMASPACE, formatdate
    import email.encoders as Encoders

from . import conf, utils

__ALL__ = ['get_template', 'send_mail']

### Template Management ###
###########################

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
    tmpl =  conf.MAIL_TMPLS.get(tmpl, default) or type_mail()
    return tmpl
    
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
    
    utils.forced_output('quick help aboot body (empty line to stop + url placeholder + \n for blank lines!)')
    body = []
    while True:
        prompt = 'body: ' if not body else '  >>> '
        line = utils.input(prompt).replace('\\n', ' ')
        body.append(line)
        if not line: break
    return {'header': header, 'body': "\n".join(body)}
    
### Email Handling ###
######################

HTML_URL_TMPL = "<a href='%s' target='_blank'>%s</a>"
URL_TAG_REGXP = re.compile(r'''[\n]?    # optional pre line break
                               %s       # actual url tag
                               [\n]?    # optional post line break
                               ''', re.VERBOSE)
    
def gen_mail(tmpl, recipients, file_):
    ''' '''
    msg = MIMEMultipart('alternative')
    msg['From']    = conf.SENDER_EMAIL
    msg['To']      = COMMASPACE.join(recipients)
    msg['Date']    = formatdate(localtime=True)
    msg['Subject'] = tmpl['header']

    # File on the local hard-drive: send it along as an attachment
    if utils.valid_local_path(file_):
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(file_, 'rb').read())
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition',
               'attachment; filename="%s"' % os.path.basename(file_))
        msg.attach(part)
        # Remove url tag from the template
        tmpl['body'] = re.sub(URL_TAG_REGXP, '', tmpl['body'])
    # File online: inject url in the template
    elif utils.valid_http_url(file_):
        html_url  = HTML_URL_TMPL % (file_, file_)
        html_body = tmpl['body']
        if '%s' in tmpl['body']:
            tmpl['body'] = tmpl['body'] % file_
            html_body    = html_body % html_url
        else:
            # append to end
            tmpl['body'] += '\n%s' % file_
            html_body    += '\n%s' % html_url
        msg.attach( MIMEText(html_body, 'html'))
            
    msg.attach( MIMEText(tmpl['body'], 'plain'))
    
    return msg

class SMTPSender(object):
    '''
    Context manager to handle errors related to the sending of emails.
    Errors should be handled in the __exit__ method.
    '''
    def __enter__(self):
        self.smtp = smtplib.SMTP(conf.SMTP_SERVR, conf.SMTP_PORT)
        # try and connect ?
        return self.smtp

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Tempo:
        #~ utils.forced_output(exc_type)
        #~ utils.forced_output(exc_val)
        #~ utils.forced_output(exc_tb)
        
        self.smtp.close()
        return True # Prevent exception propagation

def send_mail(tmpl, recipients, file_ ):
    ''' '''
    msg = gen_mail(tmpl, recipients, file_)

    with SMTPSender() as smtp:
        smtp.starttls()
        smtp.ehlo()
        login = conf.MAIL_LOGIN or utils.input("mail login: ")
        pswd  = conf.MAIL_PSWRD or getpass.getpass("mail pswd: ")
        smtp.login(login, pswd)
        res = smtp.sendmail(conf.SENDER_EMAIL, recipients, 
                            msg.as_string())
    # res contains (from python doc):
    # "a dictionary, with one entry for each recipient that was refused. 
    # Each entry contains a tuple of the SMTP error code and the 
    # accompanying error message sent by the server."
    print(res)
