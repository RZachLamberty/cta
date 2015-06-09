#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
module: config.py
author: Zach Lamberty
created: YYYY-MM-DD

Description:
    <desc>

Usage:
    <usage>

"""

import argparse


#-----------------------#
#   Module Constants    #
#-----------------------#


#-------------------------------#
#   Main routine                #
#-------------------------------#

def _parse_args():
    """Take a log file from the commmand line

    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-x", "--xample", help="An Example", action='store_true')

    args = parser.parse_args()

    return args


if __name__ == '__main__':

    args = _parse_args()

    main()
