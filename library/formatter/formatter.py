#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#     Copyright (c) 2019-2021 World Wide Technology
#     All rights reserved.
#
#     author: joel.king@wwt.com (@joelwking)
#     written:  30 August 2021
#
#     description: generates text output from dictionary
#

def format_output(query_results):
    """
    """

    print('RESULTS:\n{}'.format(yaml.dump(query_results, default_flow_style=False)))
    return