#!/bin/bash

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

wget https://data.cityofchicago.org/download/m3d6-pubu/application/xml -O $DIR/cta/data/CTARailLines.kml &&
wget https://data.cityofchicago.org/download/bs96-uama/application/xml -O $DIR/cta/data/CTARailStations.kml

exit $?
