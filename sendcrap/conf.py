#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
conf.py

Configuration loader.
All the settings from the config file will be merged into this 
namespace, so that only this file needs to be imported to access them.

Author:  raphi <r.gaziano@gmail.com>
Created: 17/04/2013
Version: 1.0
"""
import os, sys
import appdirs

APP_NAME   = "sendcrap"
APP_AUTHOR = "raphi"

APP_DIRS  = appdirs.AppDirs(APP_NAME, APP_AUTHOR)
CONF_DIR  = APP_DIRS.user_data_dir

# Create the config directory if it doesn't already exists,
# and copy the default configuration file there
if not os.path.isdir(CONF_DIR):
    import shutil
    os.makedirs(CONF_DIR)
    src_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                            'conf.py')
    shutil.copy2(src_path, os.path.join(CONF_DIR, 'config.py'))

# Import settings
sys.path.append(CONF_DIR)
from config import *

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
    
check_config()
