#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
module: googledirections.py
author: Zach Lamberty
created: 2014-01-20

Description:
    <desc>

Usage:
    <usage>

"""

import datetime
import pandas as pd
import scipy

import citybounds
import zgoogle
import ztwitter

from itertools import combinations


# --------------------- #
#   Module Constants    #
# --------------------- #


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def connect(fgoogle):
    key = zgoogle.auth.load_auth_yaml(fgoogle)['api_key']
    zgoogle.gmaps.connect(key=key)


def grid_distances(grid, mode='transit', useCache=True):
    dists = pd.DataFrame(columns=['lat0', 'lng0', 'lat1', 'lng1', 'time'])
    for ((i, r0), (j, r1)) in combinations(grid.iterrows(), 2):
        lat0 = r0['latitude']
        lng0 = r0['longitude']
        lat1 = r1['latitude']
        lng1 = r1['longitude']
        origin = '{},{}'.format(lat0, lng0)
        destination = '{},{}'.format(lat1, lng1)
        directions = zgoogle.gmaps.get_gmaps_directions(
            origin, destination, mode, useCache
        )
        time = time_from_direction(directions, mode=mode)
        dists = dists.append([{
            'lat0': lat0,
            'lng0': lng0,
            'lat1': lat1,
            'lng1': lng1,
            'time': time,
        }])
    return dists




def time_from_direction(dirs, mode="transit"):
    """ direction dict from google --> minimum distance on public transit """
    try:
        return datetime.timedelta(seconds=dirs[0]['legs'][0]['duration']['value'])
    except:
        return datetime.timedelta(seconds=0)


def get_durations_from_grid_to_grid(grid, mode="transit"):
    """ given a city grid, calculate all durations """
    x = []
    for origin in grid:
        print "origin = {}".format(origin)
        for destination in grid:
            print "destination = {}".format(destination)
            x.append({
                'oLat': origin['lat'],
                'oLng': origin['lng'],
                'oLat_ind': origin['lat_ind'],
                'oLng_ind': origin['lng_ind'],
                'dLat': destination['lat'],
                'dLng': destination['lng'],
                'dLat_ind': destination['lat_ind'],
                'dLng_ind': destination['lng_ind'],
                'duration': duration_from_direction(
                    dirs=GMAPS.directions(
                        origin=origin,
                        destination=destination,
                        mode=mode
                    ),
                    mode=mode
                ),
            })
    return x


def get_durations_from_address_to_grid(address, grid, mode="transit"):
    """ one address, grid of lat/long dicts, and a mode of transit """
    x = []
    print "origin = {}".format(address)
    for destination in grid:
        print "destination = {}".format(destination)
        x.append({
            'dLat': destination['lat'],
            'dLng': destination['lng'],
            'dLat_ind': destination['lat_ind'],
            'dLng_ind': destination['lng_ind'],
            'duration': duration_from_direction(
                dirs=GMAPS.directions(
                    origin=address,
                    destination=destination,
                    mode=mode
                ),
                mode=mode
            ),
        })
    return x


def _parse_args():
    """Take a log file from the commmand line

    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-x", "--xample", help="An Example", action='store_true')

    args = parser.parse_args()

    return args


if __name__ == '__main__':

    args = _parse_args()

    main()
