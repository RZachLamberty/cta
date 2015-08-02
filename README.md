# CTA
A while back I saw an interesting article on the ["poles of isolation" (aka "poles of inaccessability")](https://en.wikipedia.org/wiki/Pole_of_inaccessibility). The term _pole of isolation_ is a somewhat archaic term for a very landlocked place. It just so happens that my home state (South Dakota) is a particularly "isolated" place by this metric (you can see this for yourself [here](https://upload.wikimedia.org/wikipedia/commons/a/ad/Distancia_a_la_costa.png)).

This got me thinking about my *current* home, Chicago, IL. I had been talking with my wife some days prior about how awful it must be to live far from a train. In Chicago, the "El" is a modern equivalent to seafaring -- if you aren't near the el, you aren't going to get anywhere fast (if at all). The natural question, then, is what are Chicago's poles of inaccessibility?

The short answer is: exactly where you expect, and exactly where residents would need it most.


## Notes on data sources
This project is particularly indebted to the City of Chicago's awesome data portal. For the boundaries of the city I utilize a KML file created by Jonathan Levy. His map project can be found [here](https://data.cityofchicago.org/Facilities-Geographic-Boundaries/Boundaries-City/ewy2-6yfk).

I also used modified the l station and l rail line kml files to my advantage. These were also obtained through the city of chicago data portal at the following websites:

+ [L rail stations](https://data.cityofchicago.org/Transportation/CTA-L-Rail-Stations-KML-Deprecated-February-2015-/bs96-uama?)
+ [L rail lines](https://data.cityofchicago.org/Transportation/CTA-L-Rail-Lines-KML-Deprecated-February-2015-/m3d6-pubu?)


## Getting started
After you have cloned the repo, please install the conda requirements as documented in requirements.txt. Simply

```bash
cd /path/to/this/repo
conda create --name <env> --file requirements.txt
```

I am working on making this in to an actual conda package out on anaconda.org, so please bare with me.


## Working with the data
I think the [associated jupyter notebook](https://github.com/RZachLamberty/cta/blob/master/cta_demo.ipynb) is the best place to go for that, so check it out!
