NOTES_TIPS
----------

A few things learned along the way.

Stupid Windows Tricks
---------------------

Reference: https://www.pcworld.com/article/251406/windows-tips-copy-a-file-path-show-or-hide-extensions.html

Open Windows Explorer and find the photo (or document) in question.
Hold down the Shift key, then right-click the photo.
In the context menu that appears, find and click Copy as path. This copies the file location to the clipboard. 
(FYI, if you don’t hold down Shift when you right-click, the Copy as path option won’t appear.)
Press Ctrl-V to paste the text in a file. 

Mounting USB on VirtualBox
--------------------------

Mounting USB to Linux via VirtualBox to backup files - Create a device filter under USB in Virtual Box Manager

Locate the device:

    `lsblk`
or
    `sudo fdisk -l`

look for `/dev/sdb1`   - it may take a few minutes.

```bash
sudo mkdir /media/usb
sudo mount /dev/sdb1 /media/usb
sudo umount /dev/sdb1
```

Rake
----
For more information on rake-nltk, a Python implementation of the Rapid Automatic Keyword Extraction algorithm using NLTK.
refer to: https://csurfer.github.io/rake-nltk/_build/html/index.html

Converting to US-ASCII
----------------------

The metadata characters should be US-ASCII. There are also limites on the size of the metadata in the HTTP header.
https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingMetadata.html#object-metadata

https://stackoverflow.com/questions/20078816/replace-non-ascii-characters-with-a-single-space

S3Error
-------

This error:

```minio.error.S3Error: S3 operation failed; code: SignatureDoesNotMatch, message: The request signature we calculated does not match the signature you provided. Check your key and signing method.```

may be the result of non-supported data types in the meta data. For example, lists with a length of > 1.

Author
------
Joel W. King  @joelwking