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

import lxml.etree as etree
import pandas as pd
import requests
import yaml

from collections import defaultdict


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

L_URL = "https://data.cityofchicago.org/resource/8pix-ypme.json"
COLORS = ['blue', 'brn', 'g', 'o', 'p', 'pexp', 'pnk', 'red', 'y']
F_STATION_ORDER = './data/l_station_order.yaml'
F_LINES_KML = './data/CTARailLines.kml'
F_STATION_KML = './data/CTARailStations.kml'
NS = {'k': 'http://www.opengis.net/kml/2.2'}


# ----------------------------- #
#   City of chicago api         #
# ----------------------------- #

def lstation_data(lUrl=L_URL):
    """ hit up the city of chicago api for this """
    rawstations = requests.get(url=lUrl).json()
    return clean_station_data(rawstations)


def clean_station_data(stations):
    for station in stations:
        # fixing shitty station descriptive names
        sdn = station['station_descriptive_name']
        sdn = sdn.replace('  ', ' ')
        sdn = sdn.replace('Ran Ryan', 'Dan Ryan')
        station['station_descriptive_name'] = sdn

        # one color isn't tagged
        if sdn == 'Sheridan (Red Line)':
            station['red'] = True

        # blast lng/lat info into full columns
        loc = station.pop('location', {})
        station['longitude'] = float(loc['longitude'])
        station['latitude'] = float(loc['latitude'])
        station['needs_recording'] = loc.get('needs_recording', None)

        # add color column
        station['color'] = line_color(station)

    return pd.DataFrame(stations)


# ----------------------------- #
#   City of chicago kml files   #
# ----------------------------- #

def load_line_coords(fline=F_LINES_KML):
    root = etree.parse(fline)
    sublines = root.xpath(
        '/k:kml/k:Document/k:Folder/k:Placemark', namespaces=NS
    )
    x = [parse_subline(subline) for subline in sublines]

    # adding the expected hex color of the lines
    lineStyles = root.xpath('/k:kml/k:Document/k:Style', namespaces=NS)
    lineStyles = {
        ls.attrib['id']: ls.xpath('./k:LineStyle/k:color', namespaces=NS)[0].text
        for ls in lineStyles
    }

    for subline in x:
        kmlcolor = lineStyles[subline['styleUrl'].replace('#', '')]
        subline['kml_color'] = kmlcolor
        subline['rgba_color'] = {
            'r': kmlcolor[6: 8],
            'g': kmlcolor[4: 6],
            'b': kmlcolor[2: 4],
            'a': kmlcolor[0 :2],
        }

    return x


def parse_subline(subline):
    x = {}

    # regular children:
    x['name'] = subline.xpath('./k:name', namespaces=NS)[0].text
    x['styleUrl'] = subline.xpath('./k:styleUrl', namespaces=NS)[0].text

    # description is an html table with some interesting info
    descNode = subline.xpath('./k:description', namespaces=NS)[0]
    descRoot = etree.fromstring(descNode.text)
    for row in descRoot.xpath('./body/font/table/tr'):
        ds = row.xpath('./td')
        if len(ds) == 2:
            fieldname = ds[0].text
            fieldval = ds[1].text
            x[fieldname] = fieldval

    # coords
    coords = subline.xpath(
        './k:MultiGeometry/k:LineString/k:coordinates', namespaces=NS
    )[0].text.strip().split(' ')
    coords = pd.DataFrame([
        dict(zip(['longitude', 'latitude', 'altitude'], triad.split(',')))
        for triad in coords
    ]).astype(float)
    x['coords'] = coords

    return x


def load_station_coords(fstation=F_STATION_KML):
    pass


# ----------------------------- #
#   updating station dataframe  #
# ----------------------------- #

def line_color(station, colors=COLORS):
    for color in colors:
        if station.get(color, False):
            return color
    return None


def line_destination(station):
    return station.get('direction_id', None)


def station_order(fOrder=F_STATION_ORDER):
    with open(fOrder, 'rb') as f:
        return yaml.load(f)


def add_line_order(stations, stationorder):
    """ stations is a data frame with a column 'color' and another
        'station_descriptive_name'. stationorder is a dict of lists telling us
        the order of those "sdn"s. Add the index of the sdn in each color's
        list as a column in the dataframe

    """
    stations['line_order'] = stations.apply(
        func=lambda row: stationorder[row.color].index(
            row.station_descriptive_name
        ),
        axis=1
    )


def ordered_stations(stations):
    return stations.sort(columns=['color', 'line_order', 'stop_id'])
