#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
module: citibounds.py
author: Zach Lamberty
created: 2014-01-20

Description:
    Hit up the twitter / google APIs for the boundaries of 'regular' regions
    (i.e. locality / city names, neighborhoods, etc)

Usage:
    <usage>

"""

import ztwitter
import zgoogle


def get_tid_from_city(ftwitter, fgoogle, city, state):
    """ doc """
    dgoogle = zgoogle.auth.load_auth_yaml(f=fgoogle)
    lat, lng = zgoogle.gmaps.lat_lng_from_city_state(
        dgoogle['api_key'], city, state
    )
    auth = ztwitter.auth.get_oauth_from_file(ftwitter)
    return ztwitter.geo.tid_from_lat_long(auth, lat, lng)
