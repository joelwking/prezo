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
        object, and the goal is to determine how closely the search string matches the metadata.

        If we find the search string in the remote name of the presentation, these are of high relevance.
    """
    BASIC = 2.0
    FUZZ = .2
    BASELINE = 40      # Ignore scores lower than this value
    _100PCT = 100      # 100 percent

    def __init__(self, search_string, metadata, object_name):
        """
            Metadata is a list of strings
        """
        self.search_string = search_string.strip()        # Remove leading and trailing spaces
        self.metadata = self.remove_empty(metadata)       # Eliminate any empty list elements

        self.object_name = object_name                    # Remote name of the presentation
        self.in_object_name = self.found_in_remote_name()

        self.credibility_score = 0.0                      # Initialize score
        self.exact_match = 0

        self.fuzzywuzzy()

    def fuzzywuzzy(self):
        """
            Use Fuzzywuzzy to determine credibility
        """
        number_of_fuzzy_calls = 0

        for text in self.metadata:                          # Metadata is a list of strings
            for word in text.split():                       # Each line of metadata can have one or more words
                for key_word in self.search_string.split(): # The search string can have multiple words
                    score = fuzz.ratio(key_word, word)      # Compare each word in search with each word in metadata
                    if score == Credibility._100PCT:        # Returned score is a percentage from 0 to 100%
                        self.exact_match += 1               # Tally how many word by word exact matches
            score = fuzz.ratio(self.search_string, text)    # Now compare the whole search phrase with a line of metadata
            if score < Credibility.BASELINE:                # Toss out the lowscores
                continue                                    # ignore low scores
            number_of_fuzzy_calls += 1                      # Tally number of Fuzzy calls (to later calc average)
            self.credibility_score += score                 # Increment total score
        
        # Calculate the average score so we have a value not to exceed 100
        try:
            self.credibility_score = self.credibility_score / number_of_fuzzy_calls
        except ZeroDivisionError:
            self.credibility_score = 0.0
        return

    def found_in_remote_name(self):
        """
            This simple case insensitive (convert both to lower case first) 
            search using the Python substring search, return True if we find a match
            for any of the key words in the search string.
        """
        for key_word in self.search_string.split():
            if key_word.lower().strip() in self.object_name.lower():
                return True
        return False

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
            Return True or False to determine if we believe the result is credible
            Manipulate the score based on what we found from Fuzzy Wuzzy analysis
        """
        credible = False

        if self.in_object_name: 
            credible = True
            self.credibility_score += Credibility.BASELINE
        if self.exact_match:
            credible = True
            self.credibility_score += (Credibility.BASELINE / 2)
        if self.credibility_score > 0.0:
            credible = True

        self.credibility_score = round(self.credibility_score, 1)

        return credible

