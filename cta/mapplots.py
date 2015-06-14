#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: mapplots.py
Author: zlamberty
Created: 2015-06-13

Description:
    using plain-ol matplotlib to do some plotting of cta map data

Usage:
    <usage>

"""

import matplotlib


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def add_boundary(subplot, bpath, **kwargs):
    subplot.plot(bpath.longitude, bpath.latitude, **kwargs)


def add_gridpoints(subplot, grid, **kwargs):
    subplot.plot(
        grid.longitude, grid.latitude, linestyle='', marker=',', **kwargs
    )


def add_l_lines(subplot, ldatadict, line='ALL', **kwargs):
    # select the line we desire to plot (usually all)
    # order the above
    # add color based on train name (duh)
    pass
