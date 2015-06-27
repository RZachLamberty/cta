#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
module: poleofisolation.py
author: Zach Lamberty
created: 2014-01-20

Description:
    <desc>

Usage:
    <usage>

"""

import matplotlib.pyplot as plt
import scipy

import citybounds
import config
import trains
import mapplots


# --------------------- #
#   Module Constants    #
# --------------------- #


# --------------------- #
#   Main routine        #
# --------------------- #

def isolation_distances(grid, stations):
    isodists = grid.copy()
    isodists['shortest_distance'] = grid.apply(
        func=lambda row: min_distance_to_l(
            row.latitude, row.longitude, stations
        )[0],
        axis=1
    )
    return isodists


def min_distance_to_l(lat, lng, stations):
    """ calculate the nearest station to pt (lat, lng) """
    dists = distance_to_stations(lat, lng, stations)
    imin = dists.idxmin()
    d = dists[imin]
    s = stations.loc[imin]
    return d, s


def distance_to_stations(lat, lng, stations):
    # convert degrees to radians
    rlat = deg_to_rad(lat)
    rlng = deg_to_rad(lng)

    stations['rlatitude'] = stations.latitude.apply(func=deg_to_rad)
    stations['rlongitude'] = stations.longitude.apply(func=deg_to_rad)

    return stations.apply(
        func=lambda row: lat_lng_dist(rlat, rlng, row.rlatitude, row.rlongitude),
        axis=1
    )


def deg_to_rad(d):
    return d * scipy.pi / 180


def lat_lng_dist(rlat0, rlng0, rlat1, rlng1, R=config.R_IMP):
    """ haversine formula for calculating distances between lat/lng pts
        (must be in radians)!

    """
    delLat = rlat1 - rlat0
    delLng = rlng1 - rlng0
    a = (
        (scipy.sin(delLat / 2)) ** 2.
        + (scipy.cos(rlat0)) * (scipy.cos(rlat1)) * (scipy.sin(delLng / 2)) ** 2.
    )
    c = 2 * scipy.arctan2(scipy.sqrt(a), scipy.sqrt(1 - a))
    return R * c
