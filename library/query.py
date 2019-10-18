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
import pprint

import pptxindex

from fuzzywuzzy import fuzz
from fuzzywuzzy import process

DEPTH = 10

def search_keywords(pi, search_string, download_url=False):
    """
        Get all the objects in the bucket and determine if the string is in the meta data.
        input: pi: the class managing the connection to the object store
               search_string: what we are looking for in the meta data
               download_url: a boolean to flag if we want the download URL
        returns: a dictionary of results

    """
    result = dict(imdata=[])

    for object in pi.list_objects():
        (metadata, stat) = pi.get_metadata(object.object_name)
        cob = Credibility(search_string, metadata)
        if cob.credible():
            if download_url:
                url = pi.get_download_url(object.object_name)
            else:
                url = None

            result['imdata'].append(dict(object_name=object.object_name, 
                                    last_modified=object.last_modified.isoformat(),
                                    etag=object.etag,
                                    credibility=cob.credibility_score,
                                    metadata=cob.metadata,
                                    url=url))
    
    # sort the results in decending order by the credibility score
    ordered_results = sorted(result['imdata'], key = lambda i: i['credibility'], reverse=True)

    result['imdata'] = ordered_results[0:DEPTH]
    return result


class Credibility(object):
    """
    """
    BASIC = 1.0
    FUZZ = .2

    def __init__(self, search_string, metadata):
        """
        """
        self.metadata = self.remove_empty(metadata)
        self.search_string = search_string
        self.credibility_score = 0.0

        self.simple()
        self.fuzzywuzzy()

    def fuzzywuzzy(self):
        """
        """
        multiplier = Credibility.FUZZ / len(self.metadata)

        for text in self.metadata:
            score = fuzz.ratio(self.search_string, self.metadata)
            self.credibility_score = self.credibility_score + (score * multiplier)

    def simple(self):
        """
        """
        for text in self.metadata:
            if self.search_string in text:
                self.credibility_score += Credibility.BASIC

    def remove_empty(self, metadata):
        """
            remove any empty strings present in the meta data 
        """
        refreshed_metadata = []
        for item in metadata:
            if item:
                refreshed_metadata.append(item)

        return refreshed_metadata

    def credible(self):
        """
        """
        self.credibility_score = round(self.credibility_score, 1)

        if self.credibility_score <= 0.0:
            return False
        return True



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
        print ('bucket: {} does not exist or you do not have credentials for this bucket.'.format(bucket))
        exit()

    parser = argparse.ArgumentParser(description='Query metadata of object store', add_help=True)
    parser.add_argument('-u', action='store_true', default=False, dest='download_url', help='display download URL')
    parser.add_argument('-s', action='store', dest='search_string', help='search string')
    args = parser.parse_args()

    pprint.pprint(search_keywords(pi, args.search_string, download_url=args.download_url))

if __name__ == '__main__':
    main()