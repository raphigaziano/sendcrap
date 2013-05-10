#!/usr/bin/env python
#-*- coding:utf-8 -*-
MAIL_LOGIN = ""
MAIL_PSWRD = ""
SMTP_SERVR = ""
SMTP_PORT  = 0

SENDER_EMAIL = ""

# The following sizes should be given in bytes
# Use None if no max
ATTACHMENT_MAX_SIZE = 1024 * 1024 * 20  # 20 Mbs
FILE_SIZE_WARN      = 1024 * 1024 * 200 # 200 Mbs

UPLOADER = "googledrive"

CONTACTS = dict(
    bob     = "bob@bob.com",
    marylou = "hello@zerg.net",
    elvis   = "one4themon3y@pelvis.org",
    vader   = "wildchild@sithlordz.gouv",
    blondie = "sonofa***@ponchos.com"
)

GROUPS = dict(
    pals = [
        "bob",
        "vader",
        "marylou",
    ],
    work = [
        "blondie",
        "elvis",
        "bob"
    ]
)

MAIL_TMPLS = dict(
    tongs = dict(
        header = "Yo!",
        body   = '''Obi-Wan bantha Luke Skywalker R2D2 rebel spies. 
        I find your lack of faith disturbing sith lord help me Obi-Wan 
        Kenobi jawa bacta. Endor do or do not Alderaan Princess Leia 
        Organa I am your father. Scoundrel bullseye womp rats in my 
        T-16 lightsaber tie fighter Tosche Station. Tatooine I'm here 
        to rescue you may the Force be with you trench run the Force 
        star systems.'''
    ),
    another = dict(
        header = "popopo",
        body   = "GNAAAAAAAAAAAANANZNZOIJ"
    )
)

default_template = None

### Flags ###
#############

quiet     = False
verbose   = False
recursive = False
dummy     = False

### Conf checking ###
#####################

class ConfigError(AssertionError): pass

def check_config():
    ''' '''
    # All names in a group should be defined in the CONTACT dict 
    # constant.
    for group, c_list in GROUPS.items():
        for contact in c_list:
            if not contact in CONTACTS:
                raise ConfigError
    # If set, default_template should be defined in the MAIL_TMPLS dict
    if default_template is not None:
        if default_template not in MAIL_TMPLS.keys():
            raise ConfigError
    # ...
    
check_config()
