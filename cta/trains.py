#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: trains.py
Author: zlamberty
Created: 2015-06-13

Description:
    interface for cta train data

Usage:
    <usage>

"""

import requests


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

L_URL = "https://data.cityofchicago.org/resource/8pix-ypme.json"


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def lstation_data(lUrl=L_URL):
    """ hit up the city of chicago api for this """
    return requests.get(url=lUrl).json()
