import unittest
import pandas as pd
import numpy as np
import sys; sys.path.insert(0, '../')
from datafy import datafy


class TestGet(unittest.TestCase):

    def testCSV(self):
        data, type = datafy.get("https://data.cityofnewyork.us/api/views/kku6-nxdu/rows.csv?accessType=DOWNLOAD")[0]
        assert type == "csv"

    def testGeoJSON(self):
        data, type = datafy.get("https://data.cityofnewyork.us/api/geospatial/arq3-7z49?method=export&format=GeoJSON")[0]
        assert type == "geojson"

    def testJSON(self):
        data, type = datafy.get("https://data.cityofnewyork.us/api/views/kku6-nxdu/rows.json?accessType=DOWNLOAD")[0]
        assert type == "json"

    def testShapefile(self):
        ret = datafy.get("https://data.cityofnewyork.us/api/geospatial/arq3-7z49?method=export&format=Shapefile")
        assert len(list(filter(lambda d: d[1] == "shp", ret))) > 0
