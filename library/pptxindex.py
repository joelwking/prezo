#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#     Copyright (c) 2019 World Wide Technology, LLC
#     All rights reserved.
#
#     author: joel.king@wwt.com (@joelwking)
#     written:  7 October 2019
#
#     description: Python class to manage and store (Powerpoint) presentations (and other files)
#
#
#
from rake_nltk import Rake
from pptx import Presentation
from minio import Minio
from minio.error import ResponseError
import ast
from datetime import timedelta

class PresentationIndex(obj):
    """
    """
    KEYWORDS = 'x-amz-meta-keywords'                       # metadata is prepended with 'x-amz-meta-'
    S3 = 's3.amazonaws.com'

    def __init__(self, access_key=None, secret_key=None, bucket=None, cloud=PresentationIndex.S3):
        """
        """
        self.access_key = access_key
        self.secret_key = secret_key
        self.bucket = bucket
        self.minioClient = None
        self.cloud = cloud

        self.init_minio()


    def init_minio(self, secure=True):
        """
            Create an instance of the Minio client with the appropriate credentatials
        """

        self.minioClient = Minio(self.cloud, access_key=self.access_key, secret_key=self.secret_key, secure=secure)


    def verify_bucket_exists(self):
        """
            input: self.bucket 

            returns: True or False to specify if the bucket exists
        """
        for bucket in minioClient.list_buckets()
            if bucket.name == self.bucket:
                return True

        return False


    def upload_file(self, filepath=None, metadata=dict(), content_type='application/octet-stream'):
        """
            input: filepath:
                   metadata:
                   content_type: 

            returns: None indicating an error, or the etag number of the object
        """
        
        remote_name = os.path.basename(filepath)

        metadata['filepath'] = filepath

        try:
            etag = self.minioClient.fput_object(self.bucket, remote_name, filepath, metadata=metadata, content_type=content_type)
        except ResponseError as err:
            print(err)
            return None

        return etag


    def rake_it(self, input_text, depth=10):
        """
            For more information on rake-nltk, a Python implementation of the Rapid Automatic Keyword Extraction algorithm using NLTK.

            refer to: https://csurfer.github.io/rake-nltk/_build/html/index.html

            input: depth: maximum number of ranked keyword phrases to return
                   input_text: a list of sentences or text to rake.

            returns: None or a tuple of scores and phrases

        """
        
        r = Rake()
        
        if isinstance(input_text, list):
            r.extract_keywords_from_sentences(input_text)            # Extraction given the list of strings where each string is a sentence.

        if isinstance(input_text, str):
            r.extract_keywords_from_text(input_text)                 # Extraction given the text.
        else:
            return None

        if isinstance(depth, int):
            return r.get_ranked_phrases_with_scores()[0:depth]       # To get keyword phrases ranked highest to lowest with scores.
        else:
            return None


    def extract_text(self, path_to_presentation):
        """
        input: path_to_presentation: filename of the presentation to analyze

        returns: a list of the text found in the presentation

        note: text_runs will be populated with a list of strings, one for each text run in presentation
        reference: https://python-pptx.readthedocs.io/en/latest/user/quickstart.html

        """

        text_runs = []
        prs = Presentation(path_to_presentation)

        for slide in prs.slides:
            for shape in slide.shapes:
                if not shape.has_text_frame:
                    continue
                for paragraph in shape.text_frame.paragraphs:
                    for run in paragraph.runs:
                        text_runs.append(run.text)

        return text_runs


    def get_metadata(self, remote_name):
        """
            Stat the object to return the meta data

            input: remote_name: name of the object within the bucket

            returns: a tuple containing two items, a list of keywords and the stat object
                     containing the fields: 'bucket_name', 'content_type', 'etag', 'is_dir', 
                                            'last_modified', 'metadata', 'object_name', 'size'
        """

        # TODO: error checking

        stat = self.minioClient.stat_object(self.bucket, remote_name)

        keywords = ast.literal_eval(stat.metadata.get(PresentationIndex.KEYWORDS))

        return (keywords, stat)


    def get_download_url(self, remote_name, expires=1):
        """
            Get a URL which can be used to download the file even if the bucket is marked private.

            input: remote_name: name of the object within the bucket
                   self.bucket: name of the bucket

            returns: a URL

        """

        return self.minioClient.presigned_get_object(self.bucket, remote_name, expires=timedelta(days=expires)))


    def list_objects(self):
        """
            input: self.bucket: name of the bucket

            returns: a list of objects contained in the bucket

        """

        return self.minioClient.list_objects_v2(self.bucket, recursive=True)