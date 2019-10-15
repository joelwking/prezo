#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#     Copyright (c) 2019 World Wide Technology, LLC
#     All rights reserved.
#
#     author: joel.king@wwt.com (@joelwking)
#     written:  15 October 2019
#
#     description: query objects in S3 and search keywords
#
#     usage:
#        export BUCKET="name of bucket"
#        export ACCESS_KEY="<access key>"
#        export SECRET_KEY="<secret key>"
#        
#        python query.py -s 'infrastructure agility'
#
#
import os
import argparse

import pptxindex


def search_keywords(pi, search_string, download_url=False):
    """
        Get all the objects in the bucket and determine if the string is in the meta data.
    """
    for object in pi.list_objects():
        (metadata, stat) = pi.get_metadata(object.object_name)
        for text in metadata:
            if search_string in text:
                found_it()
                print '{:<40} {} etag:{:<36} bytes:{}'.format(object.object_name, object.last_modified.isoformat(), object.etag, object.size)
                try:
                    print '  {}'.format(text)
                except UnicodeEncodeError as err:
                    print '  {}'.format(err)
                if download_url:
                    print '  {}'.format(pi.get_download_url(object.object_name))

def found_it():
    """
        Determine credibility
    """
    return None

def main():
    """
        Search for the specified search string and return matching objects, optionally include a download URL
    """
    bucket = os.environ.get('BUCKET')

    pi = pptxindex.PresentationIndex(access_key=os.environ.get('ACCESS_KEY'), secret_key=os.environ.get('SECRET_KEY'), bucket=bucket)
    #
    #  First, verify we can reach the bucket specified and our credentials are configured properly.
    #
    if not pi.verify_bucket_exists():
        print 'bucket: {} does not exist or you do not have credentials for this bucket.'.format(bucket)
        exit()

    parser = argparse.ArgumentParser(description='Query metadata of object store', add_help=True)
    parser.add_argument('-u', action='store_true', default=False, dest='download_url', help='display download URL')
    parser.add_argument('-s', action='store', dest='search_string', help='search string')
    args = parser.parse_args()

    search_keywords(pi, args.search_string, download_url=args.download_url)

if __name__ == '__main__':
    main()