#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#     Copyright (c) 2019-2021 World Wide Technology
#     All rights reserved.
#
#     author: joel.king@wwt.com (@joelwking)
#     written:  18 August 2021
#
#     description: logger logic
#
#     usage:
#       >>> from logger import logger
#       >>> opts = {'logger_name': 'pony', 'file_name':'/workspaces/prezo/log/myfile.log'}
#       >>> log = logger.Logger(**opts).setup()
#       >>> log.info('foo')
#       2021-08-19 13:09:31,774 - pony - INFO - foo
#       The log message will also be written to /workspaces/prezo/log/myfile.log
#
import logging
import sys

class Logger(object):

    LOGGER_NAME = 'prezo'

    def __init__(self, logger_name=LOGGER_NAME, 
                        level=logging.INFO, 
                        file_name=None):

        self.logger_name = logger_name
        self.level = level
        self.file_name = file_name

    def setup(self):
        """
            Setup the logger object and return the object
        """
        logger = logging.getLogger(self.logger_name)
        logger.setLevel(self.level)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        sh = logging.StreamHandler(sys.stdout)
        sh.setFormatter(formatter)
        logger.handlers.clear()
        logger.addHandler(sh)

        if self.file_name:
            fh = logging.FileHandler(self.file_name)
            fh.setFormatter(formatter)
            logger.addHandler(fh)

        return logger
