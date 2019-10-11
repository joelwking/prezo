#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#     Copyright (c) 2019 World Wide Technology, LLC
#     All rights reserved.
#
#     author: joel.king@wwt.com (@joelwking)
#     written:  8 October 2019
#
#     description: sample program to demonstrate use of the class PresentationIndex
#
#     upload.py 
#
import os

import pptxindex

CUT_LINE = 9.0

def upload_file(pi, filepath):
    """
    """
    #
    # Analyze a presentation
    #
    unix_filepath = filepath.replace('\\','/')                  # filepath is in Windows format
    remote_name = os.path.basename(unix_filepath)

    prezo = '/media/usb/{}'.format(remote_name)
    pptx_text = pi.extract_text(prezo)

    #
    # Add logic to only use scores greater or equal to 9.0
    #
    keyword_list = []

    for score, text in pi.rake_it(pptx_text, depth=20):
        if score >= CUt_LINE:
            keyword_list.append(text)

    #
    # Create a dictionary of the keywords discovered by rake
    #
    rake = {pi.KW_NAME : keyword_list}
    #
    # Add the original Windows filepath 
    #
    rake['WIN_filepath'] =  filepath
    #
    # Create the metadata dictionary combining keywords from rake and core_properties of the presentation
    #
    core_properties = pi.get_core_properties(prezo)
    metadata = rake.copy()
    metadata.update(core_properties)
    #
    # Upload file and metadata
    #
    etag = pi.upload_file(filepath=prezo, metadata=metadata)

    return etag


def get_files_to_upload(ifile='upload.files'):
    """
    """
    try:
        f = open(ifile, “r”) 
    except:
        print('error reading {}'.format(ifile))
        return []

    files = f.readlines() 
    f.close()
    return files

def main():
    """
    """
    bucket = os.environ.get('BUCKET')

    pi = pptxindex.PresentationIndex(access_key=os.environ.get('ACCESS_KEY'), secret_key=os.environ.get('SECRET_KEY'), bucket=bucket)
    #
    #  First, verify we can reach the bucket specified and our credentials are configured properly.
    #
    if not pi.verify_bucket_exists():
        print 'bucket: {} does not exist or you do not have credentials for this bucket.'.format(bucket)
        exit()

    input_files = get_files_to_upload(os.environ.get('PPTX_FILES')):

    for filepath in input_files:
        upload_file(pi, filepath)

if __name__ = '__main__':
    main()