`datafy` is a small Python package that handles reading data out of a number of common formats, including recursively reading data out of archival `ZIP` files. It was written for use in a research project around open data but is provided as a separate module.

`datafy` can read data from local files:

```
>>> from datafy import get
>>> get("file:///Desktop/myfile.csv")
<<< [(<pandas DataFrame object>, "csv")]
```

As well as from the web:

```
>>> get("https://data.cityofnewyork.us/api/geospatial/arq3-7z49?method=export&format=GeoJSON")
<<< [(<geopandas GeoDataFrame object>, "geojson")]
```

It handles ZIP files as well:

```
>>> get("https://data.cityofnewyork.us/download/ft4n-yqee/application%2Fzip")
<<< [(<pandas DataFrame object>, "csv"), (<json object>, "json"), ...]
```

`pip install git+git://github.com/ResidentMario/datafy` to install.