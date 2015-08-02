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
import os
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

    isodists.loc[:, 'rlatitude'] = isodists.latitude * scipy.pi / 180
    isodists.loc[:, 'rlongitude'] = isodists.longitude * scipy.pi / 180

    stations.loc[:, 'rlatitude'] = stations.latitude * scipy.pi / 180
    stations.loc[:, 'rlongitude'] = stations.longitude * scipy.pi / 180

    i = isodists[['rlatitude', 'rlongitude']]
    statLatLngRad = stations[['rlatitude', 'rlongitude']]

    isodists.loc[:, 'shortest_distance'] = i.apply(
        func=min_distance_to_l,
        axis=1,
        statLatLngRad=statLatLngRad,
        returnImin=False,
    )
    return isodists


def min_distance_to_l(row, statLatLngRad, returnImin=False):
    """ calculate the nearest station to pt (lat, lng) """
    dists = distance_to_stations(row, statLatLngRad)
    imin = dists.argmin()
    d = dists[imin]
    if returnImin:
        return d, imin
    else:
        return d


def distance_to_stations(row, statLatLngRad, R=config.R_IMP):
    """ haversine formula for calculating distances between lat/lng pts
        (must be in radians)!

    """
    delta = statLatLngRad - row

    a =(
        scipy.sin(delta.rlatitude / 2) ** 2.
        + (
            scipy.cos(row.rlatitude)
            * scipy.cos(statLatLngRad.rlatitude)
            * (scipy.sin(delta.rlongitude / 2) ** 2.)
        )
    )

    c = 2 * scipy.arctan2(scipy.sqrt(a), scipy.sqrt(1 - a))

    return R * c
