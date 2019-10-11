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
#
import os

import pptxindex

bucket = 'joelking-presentations'

pi = pptxindex.PresentationIndex(access_key=os.environ.get('ACCESS_KEY'), secret_key=os.environ.get('SECRET_KEY'), bucket=bucket)
#
#  First, verify we can reach the bucket specified and our credentials are configured properly.
#
if not pi.verify_bucket_exists():
    print 'bucket: {} does not exist or you do not have credentials for this bucket.'.format(bucket)
    exit()
#
# Analyze a presentation
#
prezo = '/tmp/breakfast_and_learn_docker_minio.pptx'
pptx_text = pi.extract_text(prezo)


#
# Add logic to only use scores greater or equal to 9.0
#
keyword_list = []

for score, text in pi.rake_it(pptx_text, depth=20):
    if score >= 9.0:
        keyword_list.append(text)

#
# Create a dictionary of the keywords discovered by rake
#
rake = {pi.KW_NAME : keyword_list}
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
#
#
# List all the objects contained in the bucket and search metadata
#
search = 'type 1'

for object in pi.list_objects():
    (metadata, stat) = pi.get_metadata(object.object_name)
    for text in metadata:
        if search in text:
            print '{:<40} {} etag:{:<36} bytes:{}'.format(object.object_name, object.last_modified.isoformat(), object.etag, object.size)
            print '  {}'.format(text)

#
# Now provide a URL to download
#
pi.get_download_url('breakfast_and_learn_docker_minio.pptx')