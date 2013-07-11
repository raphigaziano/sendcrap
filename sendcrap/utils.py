#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
utils.py

High level utilities.

Author:  raphi <r.gaziano@gmail.com>
Created: 24/01/2013
Version: 1.0
"""
import os, sys, logging
import fnmatch
try: 
    from . import conf
except ImportError:
    # Dummy conf object for testing
    conf = type('conf', (object,), dict(quiet=False, verbose=False))
# Py2/Py3 Compatibility
if sys.version < '3':
    input = raw_input
else: input = input
    
__ALL__ = ['output', 
           'verbose_output', 
           'forced_output',
           'yes_no_prompt',
           'get_size',
           'check_size',
           'check_size_warn',
           'valid_http_url',
           'valid_local_path'
]

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
    
# adapted from:
# http://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
def cli_progressbar(label, val, end_val=100, bar_length=20):
    '''
    @TODO DOC + doctests
    '''
    percent = float(val) / end_val
    hashes = '#' * int(round(percent * bar_length))
    spaces = ' ' * (bar_length - len(hashes))
    sys.stdout.write("\r{0}[{1}] {2}%".format(label, hashes + spaces, int(round(percent * 100))))
    sys.stdout.flush()

### User Interaction ###
########################

def yes_no_prompt(msg):
    '''
    Prompt the user with a yes/no question.
    Returns True for yes, False for no.
    '''        
    prompt = input(msg).lower()
    while True:
        if prompt.startswith('y'):
            return True
        elif prompt.startswith('n'):
            return False
        else:
            prompt = input('Please answer by y(es) or n(o) ').lower()
    
### File(s) Size Utils ###
##########################
    
def get_size(*files):
    '''Return the size in bytes of all the given files.'''
    size = 0
    for f in files:
        size += os.path.getsize(f)
    return size
    
def check_size(max_, *files):
    '''
    Return False if the given files' size exceeds the conf.SIZE_WARN
    constant.
    Will return true if conf.SIZE_WARN is set to None, causing all 
    checks to pass.
    '''
    if max_ is None: 
        return True
    s = get_size(*files)
    return True if s < max_ else False

def check_size_warn(max_, *files):
    '''
    Checks the given files's list size and prompt the user for
    cancelation if size is too big.
    '''
    if check_size(max_, *files): return True
    return yes_no_prompt(
        'The given file list exceeds %s bytes.\n'
        'Are you sure you want to upload that much data ? '
        % conf.FILE_SIZE_WARN)
        
### Files listing ###
#####################

def list_files(startdir, recursive=False, abspathes=True, pattern=None):
    """
    Yield files contained in `startdir`.
    Optionnal parameters:
    `recursive`: Look for files recursively. Defaults to False.
    `abspathes`: Return absolute pathes. Defaults to True.
    """
    for f in fnmatch.filter(os.listdir(startdir),
                            pattern if pattern else '*'):
        path = os.path.join(startdir, f)
        if os.path.isfile(path):
            if abspathes:
                path = os.path.abspath(path)
            yield path
        elif recursive and os.path.isdir(path):
            for sub in list_files(path, recursive, abspathes):
                yield sub

### Path Checkers ###
######################
    
try:
    import httplib
except ImportError: # py3
    from http import client as httplib
try:
    import urlparse
except ImportError:
    from urllib import parse as urlparse

# Adapted from
# http://code.activestate.com/recipes/286225-httpexists-find-out-whether-an-http-reference-is-v/
def valid_http_url(url):
    """
    A quick and dirty way to to check whether a web file is there.

    Usage:
    >>> conf.quiet = False
    >>> valid_http_url('http://www.python.org/')
    True
    >>> valid_http_url('http://www.python.org/PenguinOnTheTelly')
    Status 404 Not Found : http://www.python.org/PenguinOnTheTelly
    False
    """
    host, path = urlparse.urlsplit(url)[1:3]
    found = False
    try:
        if url.upper()[:6] == 'HTTPS:':
            connection = httplib.HTTPSConnection(host)
        else:
            connection = httplib.HTTPConnection(host)
        #~ connection = httplib.HTTPConnection(host)  ## Make HTTPConnection Object
        connection.request("HEAD", path)
        responseOb = connection.getresponse()      ## Grab HTTPResponse Object

        if responseOb.status == 200:
            found = True
        # Redirects:
        elif responseOb.status in (301,302,):
            url = responseOb.getheader('location', '')
            return valid_http_url(url)
        else:
            output("Status %d %s : %s" % (responseOb.status, 
                                          responseOb.reason, url))
    except Exception as e:
        output("\n".join([str(e.__class__),  str(e), url]))
    return found
    
def valid_local_path(path):
    '''
    Checks whether a local file path is valid.
    
    >>> dir_ = os.path.dirname(__file__)
    >>> valid_local_path(os.path.join(dir_, 'utils.py'))
    True
    >>> valid_local_path(os.path.join(dir_, 'onoes.po'))
    False
    '''
    return os.path.isfile(path)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
