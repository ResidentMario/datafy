## datafy [![PyPi version](https://img.shields.io/pypi/v/datafy.svg)](https://pypi.python.org/pypi/pysocrata/) ![t](https://img.shields.io/badge/status-beta-yellow.svg)

`datafy` is a tiny Python package that handles reading a list of files out of a number of common formats, including 
recursively reading out the contents of a `ZIP` file.

`datafy` can read data from local files:

```
>>> from datafy import get
>>> get("file:///Desktop/myfile.csv")
<<< [{'filepath': '.',
      'mimetype': 'text/csv',
      'extension': 'csv'}]
```

As well as from the web:

```
>>> get("https://data.cityofnewyork.us/api/geospatial/arq3-7z49?method=export&format=GeoJSON")
<<< [{'filepath': '.',
      'mimetype': 'text/json',
      'extension': 'geojson'}]
```

It handles ZIP files as well:

```
>>> get("https://data.cityofnewyork.us/download/ft4n-yqee/application%2Fzip")
<<< [{'filepath': 'data.shp',
      'mimetype': 'octet/stream',
      'extension': 'shp'},
     {...}]
```

### Development

To hack on `datafy`, clone this library locally. Install its dependencies (`requests`, `requests_file`, 
`python-magic`) and development dependencies (`pytest`, `requests_mock`) via `pip`. If you have `conda`, you can run 
`conda env create -f envs/devenv.yml` to do this for you.

To execute the test suite, run `pytest tests.py` on the command line from the `/tests` folder.

Pull requests welcome.

### Limitations

* Only handles archival files in the ZIP format, so no TAR files ecetera. ([#1](https://github.com/ResidentMario/datafy/issues/1)).
* Does not handle recursively archived files ([#2](https://github.com/ResidentMario/datafy/issues/2)).
