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
