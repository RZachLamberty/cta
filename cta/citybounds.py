#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
module: citibounds.py
author: Zach Lamberty
created: 2014-01-20

Description:
    utility functions for working with the boundaries for a city. Presumably
    this is for Chicago, but if I abstract it it can be general enough

Usage:
    <usage>

"""

import matplotlib.path as mplpath
import pandas as pd
import scipy


# --------------------- #
#   Module Constants    #
# --------------------- #

FCHICAGO = './data/chicago_boundaries.csv'
NBINS = 100


# --------------------- #
#   boundary functions  #
# --------------------- #

def load_boundary(f=FCHICAGO):
    """ load the file f, into a scipy array

        I have collected the bounding points of the city of Chicago into a
        csv file. They were originally found in a KLM file created by
        Jonathan Levy. His map project can be found here:

            https://data.cityofchicago.org/Facilities-Geographic-Boundaries/Boundaries-City/ewy2-6yfk

    """
    return pd.read_csv(f)


def path_to_poly(path):
    return mplpath.Path(path)


def within_boundary(lat, lng, boundary):
    """ determine whether a given lat/lng point is within a boundary """
    return bool(boundary.contains_point((lat, lng)))


# --------------------- #
#   grid building       #
# --------------------- #

def build_grid(f=FCHICAGO, latbins=NBINS, lngbins=NBINS,
               allowOutsideBoundary=False):
    """ given a file f which contains (pref csv) data of a city's boundaries,
        and latbins, lngbins, the number of bins we wish to have in each
        direction, return an iterable of (lat, lng) pairs which fall on the bin
        gridlines and within the boundary of the city

    """
    bpath = load_boundary(f)
    bpoly = path_to_poly(bpath)

    latmax = bpath.latitude.max()
    latmin = bpath.latitude.min()
    lngmax = bpath.longitude.max()
    lngmin = bpath.longitude.min()

    latspace = scipy.linspace(latmin, latmax, num=latbins)
    lngspace = scipy.linspace(lngmin, lngmax, num=lngbins)

    return pd.DataFrame(
        (
            [lat, lng] for lat in latspace for lng in lngspace
            if (allowOutsideBoundary) or within_boundary(lat, lng, bpoly)
        ),
        columns=['latitude', 'longitude']
    )
