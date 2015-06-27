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
import scipy

import config as CONFIG


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

L_LINE_COLOR_MAPPING = CONFIG.color_codes()


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def add_boundary(subplot, bpath, **kwargs):
    subplot.plot(bpath.longitude, bpath.latitude, **kwargs)


def add_gridpoints(subplot, grid, **kwargs):
    subplot.plot(
        grid.longitude, grid.latitude, linestyle='', marker=',', **kwargs
    )


def add_stations(subplot, stations, **kwargs):
    for (colorname, d) in L_LINE_COLOR_MAPPING.items():
        colorcode = d['api_code']
        plotcolor = d['hex']
        lline = stations[stations.color == colorcode]
        subplot.plot(
            lline.longitude, lline.latitude, color=plotcolor, marker='o',
            mec='k', linestyle='', **kwargs
        )


def add_l_lines(subplot, llines, **kwargs):
    for lline in llines:
        coords = lline['coords']
        rgba = lline['rgba_color']
        rgb = '#{r:}{g:}{b:}'.format(**rgba)
        subplot.plot(coords.longitude, coords.latitude, color=rgb, **kwargs)


def add_isolation_dist_contours(fig, subplot, isodists, N=10, **kwargs):
    """ contour plot of distances to l stations """
    ipiv = isodists.pivot('longitude', 'latitude')
    x = ipiv.columns.levels[1].values
    y = ipiv.index.values
    z = ipiv.values
    xi, yi = scipy.meshgrid(x, y)
    c = subplot.contour(yi, xi, z, N, **kwargs)
    cbar = fig.colorbar(c)
    cbar.ax.set_ylabel('Miles', rotation=270)


def add_isolation_dist_colormap(fig, subplot, isodists, N, **kwargs):
    """ filled contour plot of distances to l stations """
    ipiv = isodists.pivot('longitude', 'latitude')
    x = ipiv.columns.levels[1].values
    y = ipiv.index.values
    z = ipiv.values
    xi, yi = scipy.meshgrid(x, y)
    c = subplot.contourf(yi, xi, z, N, **kwargs)
    cbar = fig.colorbar(c)
    cbar.ax.set_ylabel('Miles', rotation=270)


def main():
    import citybounds
    import trains

    # getting plot data
    bpath = citybounds.load_boundary()
    grid = citybounds.build_grid()
    stations = trains.lstation_data()
    stationorder = trains.station_order()
    trains.add_line_order(stations, stationorder)
    orderedstations = trains.ordered_stations(stations)
    llines = trains.load_line_coords()
    isodists = poleofisolation.isolation_distances(grid, stations)

    # plotting
    f = plt.figure()
    s = f.add_subplot(111)
    mapplots.add_isolation_dist_colormap(f, s, isodists, N=50)
    mapplots.add_boundary(s, bpath)
    mapplots.add_stations(s, orderedstations)
    mapplots.add_l_lines(s, llines)
    s.set_xlabel("longitude")
    s.set_ylabel("latitude")
    s.set_title("Poles of Isolation")

    f.show()
    return f


# ----------------------------- #
#   command line                #
# ----------------------------- #

if __name__ == '__main__':

    main()
