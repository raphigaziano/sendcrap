#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
sendcrap.py

Program entry point.

Author:  raphi <r.gaziano@gmail.com>
Created: 19/01/2013
Version: 1.0
"""
import sys
import importlib
from . import utils, args, tar, mail
# checking conf file on startup
try:
    from . import conf
except (SyntaxError, AssertionError) as e:
    utils.forced_output("Conf Error!")
    utils.forced_output(str(e))
    sys.exit(1)
try:
    uploader = importlib.import_module(
        'sendcrap.uploaders.%s' % conf.UPLOADER)
except ImportError:
    utils.forced_output("Conf Error!")
    utils.forced_output("No module named %s was found in the uploaders "
                        "package" % conf.UPLOADER)
    sys.exit(1)
    

def main():
    opts = args.parse_args()
    f, m = args.process_args(opts)
    #~ f, m = args.process_args()
    
    if conf.dummy: 
        summary = 'uploading files:\n\t%s\nnotifying:\n\t%s' % (
            ",\n\t".join(f) if f else 'None', 
            ",\n\t".join(m) if m else 'None'
        )
        utils.forced_output(summary)
        return 0
    
    try:
        tar_path = tar.write(opts.dir, *f)
    except SystemExit: # User cancelled
        return 0
        # + Errors
    
    template = mail.get_template(opts.template)
    # @TODO: Check for exe in tar (stoopid gmail!)
    if not utils.check_size(conf.ATTACHMENT_MAX_SIZE, *f):
        tar_path = uploader.upload_file(tar_path)
        
    if template is not None: 
        mail.send_mail(template, m, tar_path)
        
    # Exit code, picked up by sys.exit
    return 0
    
    
if __name__ == "__main__":
    sys.exit(main())
