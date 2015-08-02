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

import csv
import matplotlib.path as mplpath
import os
import pandas as pd
import scipy

from lxml import etree
from config import HERE


# --------------------- #
#   Module Constants    #
# --------------------- #

FKML = os.path.join(HERE, 'data', 'chicago_boundaries.kml')
FCSV = os.path.join(HERE, 'data', 'chicago_boundaries.csv')
NBINS = 100
CTA_NS = {'cta': 'http://www.opengis.net/kml/2.2'}


# --------------------- #
#   boundary functions  #
# --------------------- #

def kml_to_csv(fkml=FKML, fcsv=FCSV):
    """ load the kml file downloaded from the city of chicago open data portal
        and turn it into a csv. I just find this much cleaner to work with, in
        the long run

    """
    x = etree.parse(fkml)
    rings = x.xpath(
        '//cta:MultiGeometry/cta:Polygon/*/*/cta:coordinates',
        namespaces=CTA_NS
    )

    output = []
    for (i, ring) in enumerate(rings):
        coordpairs = ring.text.split(' ')
        for cp in coordpairs:
            lng, lat = cp.split(',')
            output.append({'loop': i, 'latitude': lat, 'longitude': lng})

    with open(fcsv, 'wb') as f:
        c = csv.DictWriter(f, fieldnames=['loop', 'latitude', 'longitude'])
        c.writeheader()
        c.writerows(output)


def load_boundary(f=FCSV):
    """ load the file f, into a scipy array

        I have collected the bounding points of the city of Chicago into a
        csv file. They were originally found in a KLM file created by
        Jonathan Levy. His map project can be found here:

            https://data.cityofchicago.org/Facilities-Geographic-Boundaries/Boundaries-City/ewy2-6yfk

    """
    return pd.read_csv(f)


def path_to_polys(path):
    grouped = path.groupby('loop')
    f = grouped.first()
    return grouped.apply(mplpath.Path)


def within_boundary(lat, lng, boundary):
    """ determine whether a given lat/lng point is within a boundary """
    return any(path.contains_point((lat, lng)) for path in boundary.values)


# --------------------- #
#   grid building       #
# --------------------- #

def build_grid(f=FCSV, latbins=NBINS, lngbins=NBINS, allowOutsideBoundary=False):
    """ given a file f which contains (pref csv) data of a city's boundaries,
        and latbins, lngbins, the number of bins we wish to have in each
        direction, return an iterable of (lat, lng) pairs which fall on the bin
        gridlines and within the boundary of the city

    """
    bpath = load_boundary(f)
    bpoly = path_to_polys(bpath)

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
