#!/bin/bash

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

echo "******"
echo ""
echo "Collecting cta el station data from data.cityofchicago.org"
echo ""
echo "******"
mkdir -p $DIR/cta/data &
wget https://data.cityofchicago.org/download/m3d6-pubu/application/xml -O $DIR/cta/data/CTARailLines.kml &
wget https://data.cityofchicago.org/download/bs96-uama/application/xml -O $DIR/cta/data/CTARailStations.kml &
wget https://data.cityofchicago.org/api/geospatial/ewy2-6yfk?method=export\&format=KML -O $DIR/cta/data/chicago_boundaries.kml

exit $?
