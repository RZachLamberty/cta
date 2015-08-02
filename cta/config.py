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

import os
import yaml


# --------------------- #
#   Module Constants    #
# --------------------- #

HERE = os.path.dirname(os.path.realpath(__file__))
COLORYAML = os.path.join(HERE, 'config', 'line_colors.yaml')
R_METRIC = 6378.1  # km
R_IMP = 3963.1676  # miles


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def color_codes(f=COLORYAML):
    with open(f, 'rb') as fin:
        return yaml.load(fin)
