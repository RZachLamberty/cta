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
import googlemaps
import scipy

import citybounds

from authkeys import GOOGLE_API_KEY


#-----------------------#
#   Module Constants    #
#-----------------------#

N_BINS = 100

GMAPS = googlemaps.Client(key=GOOGLE_API_KEY)


#-------------------------------#
#   Main routine                #
#-------------------------------#

def build_city_grid(city, state, nLat=N_BINS, nLng=N_BINS):
    """ hit up google for the bounding borders of a city, then divide up the
        resulting rectangle into some number of squares

    """
    xMax, xMin, yMax, yMin = citybounds.get_google_bounding_box(
        city=city,
        state=state
    )

    return [
        {'lat_ind': j, 'lat': lat, 'lng_ind': i, 'lng': lng}
        for (i, lng) in enumerate(scipy.linspace(start=xMin, stop=xMax, num=nLat))
        for (j, lat) in enumerate(scipy.linspace(start=yMin, stop=yMax, num=nLng))
    ]


def duration_from_direction(dirs, mode="transit"):
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
