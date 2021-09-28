NOTES_TIPS
----------
A few things learned along the way.

Creating an input inventory file
--------------------------------
In this example, I created a target directory `~/prezo/data` and copied all the files with an extension of `.pptx` to the target directory.

`scp ./AnsibleFest2018/*.pptx administrator@olive-iron.sandbox.wwtatc.local:prezo/data/`

Create your `upload.file` to create an inventory of the files to be uploaded.

Enter the directory where you copied the files (`~/prezo/data`). Create the inventory file and prepend the directory of the container volume.

```shell
~/prezo/data$ ls >>upload.files
```
Using `vi` as an editor, you can prepend the container path to all the lines in the inventory file.

```vi
:%s!^!/opt/powerpoint/!
```
Then save the modified file. You have created an inventory file listing the full path of the file(s) you wish to upload.

Stupid Windows Tricks
---------------------
How to locate the file path in Windows.

Reference: https://www.pcworld.com/article/251406/windows-tips-copy-a-file-path-show-or-hide-extensions.html

* Open Windows Explorer and find the photo (or document) in question.
* Hold down the Shift key, then right-click the photo.
* In the context menu that appears, find and click Copy as path. This copies the file location to the clipboard. (FYI, if you don’t hold down Shift when you right-click, the Copy as path option won’t appear.)
* Press Ctrl-V to paste the text in a file. 

Mounting USB on VirtualBox
--------------------------
Mounting USB to Linux via VirtualBox to access files from the virtual machine.

Attach the USB drive to your system. Wait for the Operating System to recognize the removable media.

Use the VirtualBox Manager, Select USB, then create (add) a device filter, selecting the USB drive shown in the dialog box.

>Note: you must power off the virtual machine in Virtual Box Manager and power on after the filter has been created for the USB drive to be recognized by the Linux OS.

Locate the device using either of these Linux commands:

    `lsblk`
or

    `sudo fdisk -l`

look for `/dev/sdb1`  - it may take a few minutes. 

```
NAME                      MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
sda                         8:0    0   16G  0 disk 
├─sda1                      8:1    0    1M  0 part 
├─sda2                      8:2    0    1G  0 part /boot
└─sda3                      8:3    0   15G  0 part 
  └─ubuntu--vg-ubuntu--lv 253:0    0   15G  0 lvm  /
sdb                         8:16   1 14.9G  0 disk 
└─sdb1                      8:17   1 14.9G  0 part 
sr0                        11:0    1 1024M  0 rom  
```
Create a mount point and mount the media:

```bash
sudo mkdir /media/usb
sudo mount /dev/sdb1 /media/usb
```

After mounting, the mount point is shown:

```
administrator@flint:~$ lsblk
NAME                      MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
sda                         8:0    0   16G  0 disk 
├─sda1                      8:1    0    1M  0 part 
├─sda2                      8:2    0    1G  0 part /boot
└─sda3                      8:3    0   15G  0 part 
  └─ubuntu--vg-ubuntu--lv 253:0    0   15G  0 lvm  /
sdb                         8:16   1 14.9G  0 disk 
└─sdb1                      8:17   1 14.9G  0 part /media/usb
sr0                        11:0    1 1024M  0 rom  
```

You can unmount the device using the command:

```bash
sudo umount /dev/sdb1
```

Rake
----
For more information on rake-nltk, a Python implementation of the Rapid Automatic Keyword Extraction algorithm using NLTK.
refer to: https://csurfer.github.io/rake-nltk/_build/html/index.html

Converting to US-ASCII
----------------------
Metadata characters must be US-ASCII. There are also limits on the size of the metadata in the HTTP header.

https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingMetadata.html#object-metadata

https://stackoverflow.com/questions/20078816/replace-non-ascii-characters-with-a-single-space

S3Error
-------
This error:

```minio.error.S3Error: S3 operation failed; code: SignatureDoesNotMatch, message: The request signature we calculated does not match the signature you provided. Check your key and signing method.```

is the result of non-supported data types in the meta data. For example, lists with a length of > 1.

Author
------
Joel W. King  @joelwking