## About

`datafy` is a small Python package that handles reading a list of files out of a number of common formats, including 
recursively reading out the contents of a `ZIP` file.

`datafy` can read data from local files:

```
>>> from datafy import get
>>> get("file:///Desktop/myfile.csv")
<<< TODO
```

As well as from the web:

```
>>> get("https://data.cityofnewyork.us/api/geospatial/arq3-7z49?method=export&format=GeoJSON")
```

It handles ZIP files as well:

```
>>> get("https://data.cityofnewyork.us/download/ft4n-yqee/application%2Fzip")
```

## Installation
`pip install git+git://github.com/ResidentMario/datafy` to install. A PyPi release is still forthcoming.

## Development

To hack on `datafy`, clone this library locally. Install its dependencies (`requests`, `requests_file`, 
`python-magic`) and development dependencies (`pytest`, `requests_mock`) via `pip`. If you have `conda`, you can run 
`conda env create -f envs/devenv.yml` to do this for you.

To execute the test suite, run `pytest tests.py` on the command line from the `/tests` folder.

Pull requests welcome.