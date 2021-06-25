#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#     Copyright (c) 2019-2021 World Wide Technology
#     All rights reserved.
#
#     author: joel.king@wwt.com (@joelwking)
#     written:  8 October 2019, revised 27 May 2021
#
#     description: Program to analyze and upload PowerPoint presentations to object store.
#
#     usage:
#        export BUCKET="name of bucket"
#        export ACCESS_KEY="<access key>"
#        export SECRET_KEY="<secret key>"
#        export PPTX_FILES='data/upload.files'
#        export CUT_LINE=9.0
#        python3 library/upload.py 
#
import os
import pptxindex

try: 
    CUT_LINE = float(os.environ.get('CUT_LINE', 9.0))
except ValueError:
    CUT_LINE = 9.0
    print('ENV:WARN ... could not convert value of CUT_LINE to float, using {}'.format(CUT_LINE))

def upload_file(pi, filepath):
    """
        Extract the text from the presentation. Use Rake to return the score and text. If the text
        is deemed sufficiently relevant, append it to the list of keywords.

        Retrieve the core_properties from the presentation, and use this along with the keywords as metadata.
        Validate the metatdata. Upload the file as an object in the target bucket.
    """
    keyword_list = []
    pptx_text = pi.extract_text(filepath)                  # Extract the text from the file
    for score, text in pi.rake_it(pptx_text, depth=20):
        if score >= CUT_LINE:                              # Determine if this is relevant based on derived score
            keyword_list.append(text)

    #
    # Create a dictionary of the keywords discovered by rake
    #
    rake = {pi.KW_NAME : keyword_list}
    #
    # Create the metadata dictionary combining keywords from rake and core_properties of the presentation
    #
    core_properties = pi.get_core_properties(filepath)

    metadata = rake.copy()
    metadata['filepath'] =  filepath
    metadata.update(core_properties)

    for key, value in metadata.items():
        if isinstance(value, (str, float, int)):
            try:
                metadata[key] = pi.us_ascii([value])
            except TypeError as err:
                print('UPLOAD_FILE:WARN ... encountered TypeError {} {} {}'.format(type(value), key, value))
        elif isinstance(value, list):
            metadata[key] = pi.us_ascii(value)
        else:
            print('UPLOAD_FILE:WARN ... unrecognized datatype {} {} {}'.format(type(value), key, value))
    #
    # Upload file and metadata
    #
    result = pi.upload_file(filepath=filepath, metadata=metadata)

    return result

def get_files_to_upload(ifile='upload.files'):
    """
        Input: ifile: Name of text file with the full path of the file(s) to upload
        Returns: Empty list or List of files
    """
    try:
        f = open(ifile, 'r')
    except:
        print('GET_FILES_TO_UPLOAD:ERROR error reading {}'.format(ifile))
        return []

    files = f.readlines() 
    f.close()
    return files

def main():
    """
        Instanciate a connection object with the keys and name of the bucket. Verify the bucket exists,
        ensuring that we can reach the bucket specified with the credentials provided.
        Get a list of files to upload, and call method `upload file` to create the metadata and upload
        the file to the object store.
    """
    pi = pptxindex.PresentationIndex(access_key=os.environ.get('ACCESS_KEY'), 
                                     secret_key=os.environ.get('SECRET_KEY'), 
                                     bucket=os.environ.get('BUCKET'))

    if not pi.verify_bucket_exists():
        print('MAIN:ERROR bucket {} does not exist or you do not have credentials for this bucket.'.format(bucket))
        exit()

    input_files = get_files_to_upload(os.environ.get('PPTX_FILES'))

    if not input_files:
        print("MAIN:ERROR {}".format('No files to upload!'))

    for filepath in input_files:
        result = upload_file(pi, filepath)
        if not result:
            result = pi.error_message
            print("MAIN:ERROR {} {}".format(result, filepath))
        else:
            print("MAIN:OK etag:{} filepath:{}".format(result.etag, filepath))

if __name__ == '__main__':
    main()