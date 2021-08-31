#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#     Copyright (c) 2019 World Wide Technology
#     All rights reserved.
#
#     author: joel.king@wwt.com (@joelwking)
#     written:  15 October 2019
#
#     description: determine credibility score if a string exists in metadata
#
from fuzzywuzzy import fuzz
# from fuzzywuzzy import process

class Credibility(object):
    """
        Class using FuzzyWuzzy Python library to determine a credibility score to determine
        how closely two strings match. In our use case, we have metadata assocated with an
        object, and the goal is to determine how closely the search string matches the metadata
    """
    BASIC = 1.0
    FUZZ = .2

    def __init__(self, search_string, metadata):
        """
            Metadata is a list of strings
        """
        self.metadata = self.remove_empty(metadata)
        self.search_string = search_string.strip()
        self.credibility_score = 0.0

        self.simple()
        self.fuzzywuzzy()

    def fuzzywuzzy(self):
        """
            Use Fuzzywuzzy to determine credibility
        """
        multiplier = Credibility.FUZZ / len(self.metadata)

        for text in self.metadata:
            score = fuzz.ratio(self.search_string, self.metadata)
            self.credibility_score = self.credibility_score + (score * multiplier)

    def simple(self):
        """
            This simple search uses the Python substring search. If the string is located,
            we increment the credibility score.
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

