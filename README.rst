sendcrap
========

sendcrap is a small command line utility to automate sending a bunch of
files to various people.

It packs all the specified files (by default, all files contained in 
the working directory) in a tar.gz archive, upload this to google drive
if the size exceeds 20Mbs or so, and then send a mail with the google
drive url to a preset number of adresses.

I'm tailoring it to my specific needs, so i don't know if it'll be of
any real use to anyone else. I might try and make the upload to gdrive
part easy to replace with something else if i feel like it, but i 
probably won't bother testing that much. If anyone happens to be 
interested, tho, feel free to hack the crap out of this and let me know 
how it's going ;) 

I'm planning on using a simple configuration format and options system
so the other options are easy to override. 

I'm barely getting started and am not sure how the damn thing will 
actually work when it's done, so i'll update this readme with moar doc
when i actually get a clue.

I'm developping with Python 2.7. I'll probably try and make it 
compatible with py3.2, but I'll bother when the basic thing is done.

Also, i'm planning on using the clint library, because it's got an 
awesome name, so that'll be at least one dependency. We'll see about 
others later.


Compatibility notes:
--------------------

- The linux argparse module for python 3.2 seems to have an import bug
  that is causing one of the parser tests to fail.
  The quick and dirty fix involves hacking the argparse file directly:
  Line 93, replace the line ::
  
    from gettext import gettext

  with::
    
    from gettext import gettext, ngettext
    
  This problem does not occur on windows.
  
- Argument parsing requires the argparse module, which thus becomes an
  additional dependency for py 2.6.
  
  Installing the backported version manually works ok, despite a small 
  difference with the standard version, causing one test to fail:
  mutually explusive flags don't seem to work, and sending both the
  -v and -q flags do not crash the app as expected.
  
- tarfile objects do not support context managers with 2.6.
  This will be fixed soon.
