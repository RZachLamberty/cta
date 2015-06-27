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

import yaml


# --------------------- #
#   Module Constants    #
# --------------------- #

COLORYAML = './config/line_colors.yaml'
R_METRIC = 6378.1  # km
R_IMP = 3963.1676  # miles


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def color_codes(f=COLORYAML):
    with open(f, 'rb') as fin:
        return yaml.load(fin)
