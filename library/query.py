#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#     Copyright (c) 2021 World Wide Technology
#     All rights reserved.
#
#     author: joel.king@wwt.com (@joelwking)
#     written:  15 October 2019, revised 18 August 2021
#
#     description: query objects in S3 and search keywords
#
#     usage:
#        export BUCKET="name of bucket"
#        export ACCESS_KEY="<access key>"
#        export SECRET_KEY="<secret key>"
#        
#        python library/query.py -u -s 'infrastructure agility'
#
#
import os
import argparse
import yaml

import pptxindex
from credibility import Credibility

from logger import logger

log = logger.Logger(logger_name='query', level=20).setup()

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
                url = '... specify the -u argument for a download URL'

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


def main():
    """
        Search for the specified search string and return matching objects, optionally include a download URL
    """
    #
    #  Get the arguments
    #
    parser = argparse.ArgumentParser(description='Query metadata of object store', add_help=True)
    parser.add_argument('-u', action='store_true', default=False, dest='download_url', help='display download URL')
    parser.add_argument('-s', action='store', dest='search_string', help='search string (use lowercase)')
    args = parser.parse_args()

    options = dict(
        bucket=os.environ.get('BUCKET', 'nobucket'),
        access_key=os.environ.get('ACCESS_KEY', 'noaccesskey'),
        secret_key=os.environ.get('SECRET_KEY', 'nosecret'))

    pi = pptxindex.PresentationIndex(**options)
    #
    #  Verify we can reach the bucket specified and our credentials are configured properly.
    #
    if not pi.verify_bucket_exists():
        log.error('MAIN: bucket {} does not exist or you do not have credentials for this bucket.'.format(options['bucket']))
        exit()

    result = search_keywords(pi, args.search_string, download_url=args.download_url)
    log.info('RESULTS:\n{}'.format(yaml.dump(result['imdata'], default_flow_style=False)))

if __name__ == '__main__':
    main()
