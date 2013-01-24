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
# checking conf file on startup
try:
    import conf
except (SyntaxError, AssertionError) as e:
    print("Conf Error!")
    print(str(e))
    sys.exit(1)

from . import utils, args

def main():
    #~ opts = args.parse_args()
    #~ f, m = args.process_args(opts)
    f, m = args.process_args()
    
    summary = 'uploading files:\n\t%s\nnotifying:\n\t%s' % (
        ",\n\t".join(f) if f else 'None', 
        ",\n\t".join(m) if m else 'None'
    )
    if conf.dummy: 
        utils.forced_output(summary)
        return 0
    utils.verbose_output(summary)
    
    
    # Exit code, picked up by sys.exit
    return 0
    
    
if __name__ == "__main__":
    sys.exit(main())
