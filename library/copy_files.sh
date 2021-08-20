#!/bin/bash
#
#     Copyright (c) 2021 World Wide Technology
#     All rights reserved.
#
#     author: joel.king@wwt.com (@joelwking)
#     written:  20 August 2021
#
#     description: builds a series of commads to copy files into the 
#                  container's workspace for testing
#
#     usage:
#       locate the powerpoint files on your file system
#           % find . -type f | grep ".pptx"
#       edit the output to include the absolute path of the files, for example
#
#          /Users/kingjoe/Documents/WWT/NS_VT_Calls/__Traffic_Analysis/NS_VT_Veterans_Day.pptx
#
#       then cat the file and pipe into this script,
#
#          library# cat ../data/files_to_upload.txt | bash copy_files.sh
# 
#       the output will be as:
#  
#          cp -p  /Users/kingjoe/Documents/WWT/NS_VT_Calls/__Traffic_Analysis/NS_VT_Veterans_Day.pptx data/NS_VT_Veterans_Day.pptx
#
#       this copies files into the Development environment for testing.
#
while IFS= read -r line; do
  fbname=$(basename "$line")
  printf "cp -p  %s data/%s\n" "$line" "$fbname"
done


