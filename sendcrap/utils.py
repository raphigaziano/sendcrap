#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
utils.py

High level utilities.

Author:  raphi <r.gaziano@gmail.com>
Created: 24/01/2013
Version: 1.0
"""
import sys, logging
try: 
    import conf
except ImportError:
    # Dummy conf object for testing
    conf = type('conf', (object,), dict(quiet=False, verbose=False))
    
__ALL__ = ['output', 'verbose_output', 'forced_output']

### Output handling ###
#######################

# from: 
# http://code.activestate.com/recipes/576819-logging-to-console-without-surprises/
class ConsoleHandler(logging.StreamHandler):
    """A handler that logs to console in the sensible way.

    StreamHandler can log to *one of* sys.stdout or sys.stderr.

    It is more sensible to log to sys.stdout by default with only error
    (logging.ERROR and above) messages going to sys.stderr. This is how
    ConsoleHandler behaves.
    """

    def __init__(self):
        logging.StreamHandler.__init__(self)
        self.stream = None # reset it; we are not going to use it anyway
        
    def emit(self, record):
        if record.levelno >= logging.ERROR:
            self.__emit(record, sys.stderr)
        else:
            self.__emit(record, sys.stdout)

    def __emit(self, record, strm):
        self.stream = strm
        logging.StreamHandler.emit(self, record)

    def flush(self):
        # Workaround a bug in logging module
        # See:
        #   http://bugs.python.org/issue6333
        if self.stream and hasattr(self.stream, 'flush') and not self.stream.closed:
            logging.StreamHandler.flush(self)

#-- Logger setup
_logger = logging.getLogger('logger')
_formatter = logging.Formatter('%(message)s')
_handler = ConsoleHandler()
_handler.setFormatter(_formatter)
_logger.addHandler(_handler)
_logger.setLevel(logging.INFO)

def _output(msg):
    ''' 
    Low-level print like function.
    Logs the given message.
    
    @param msg: string to be logged.
    '''
    _logger.info(msg)

#-- Public output functions

def output(msg):
    '''
    Logs the given message if the quiet option is not set.
    
    @param msg: string to be logged.
    
    >>> conf.quiet = False
    >>> output('message')
    message
    >>> conf.quiet = True
    >>> output('message')
    >>>
    '''
    if conf.quiet: return
    return _output(msg)
    
def verbose_output(msg):
    '''
    Logs the given message only if the verbose option is set.
    
    @param msg: string to be logged.
    
    >>> conf.verbose = False
    >>> verbose_output('message')
    >>>
    >>> conf.verbose = True
    >>> verbose_output('message')
    message
    '''
    if not conf.verbose: return
    return _output(msg)
    
def forced_output(msg):
    ''' 
    Logs the given message, whether the quiet option is set or not.
    
    @param msg: string to be logged.
    
    >>> conf.quiet = False
    >>> forced_output('message')
    message
    >>> conf.quiet = True
    >>> forced_output('message')
    message
    '''
    return _output(msg)
    

if __name__ == '__main__':
    import doctest
    doctest.testmod()
