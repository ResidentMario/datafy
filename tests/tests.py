import unittest
import requests_mock
import pytest
import re

import sys; sys.path.insert(0, '../')
from datafy import datafy


# Helpers.
def read_file(fp):
    """Read a file from the /data folder as string."""
    with open('data/' + fp, 'rb') as f:
        return f.read()


def ok(results):
    """Return whether or not all results are status 200 OK."""
    return all([result['data'].ok for result in results])


def match(results, expected):
    """Return whether or not the results match the expectation. Excludes the response object."""
    for result in results:
        result.pop('data')
    return results == expected


# Tests
@pytest.mark.parametrize("uri,filename,type_hints", [
    ('mock://data.cityofnewyork.us/api/views/kku6-nxdu/rows.csv?accessType=DOWNLOAD',
     'Demographic Statistics By Zip Code.csv',
     ('text/csv', 'csv')),
    ('mock://data.cityofnewyork.us/api/geospatial/arq3-7z49?method=export&format=GeoJSON',
     'Subway Stations.geojson',
     ('application/geo+json', 'geojson')),
    ('mock://data.cityofnewyork.us/api/views/kku6-nxdu/rows.json?accessType=DOWNLOAD',
     'Demographic Statistics By Zip Code.json',
     ('application/json', 'json'))
])
def test_core_files(uri, filename, type_hints):
    """Test that the core method works with a variety of non-archival input filetypes."""
    with requests_mock.Mocker() as mock:
        if type_hints[1] == 'zip':
            import pdb; pdb.set_trace()

        # Interdict network requests to retrieve data from the localized store instead.
        mock.get(uri, content=read_file(filename))

        results = datafy.get(uri, request_filesize=False, type_hints=type_hints)
        assert ok(results)
        expected = [{'filepath': '.', 'mimetype': type_hints[0], 'extension': type_hints[1]}]
        assert match(results, expected)


# TODO: Finish implementing this.
# @pytest.mark.parametrize("uri,filename,type_hints", [
#     ('mock://data.cityofnewyork.us/api/geospatial/arq3-7z49?method=export&format=Shapefile', 'Subway Stations.zip',
#     ('application/zip', 'zip'))
# ])
# def test_core_archival_formats(uri, filename, type_hints):
#     """Test that the core method works with a variety of non-archival input filetypes."""
#     with requests_mock.Mocker() as mock:
#
#         # Interdict network requests to retrieve data from the localized store instead.
#         mock.get(uri, content=read_file(filename))
#         # Interdict local file requests (occurs when running on an achival file).
#         mock.get(re.compile('^file:\/\/\/\d*\/[\s\S]*.[\s\S]*'), content=b'whatever')
#
#         results = datafy.get(uri, request_filesize=False, type_hints=type_hints)
#         assert ok(results)
#         expected = [{'filepath': '.', 'mimetype': type_hints[0], 'extension': type_hints[1]}]
#         assert match(results, expected)


# TODO: Finish stripping these out into pytest parameterized tests.
class TestGet(unittest.TestCase):
    """Test that the core method works with a variety of input filetypes."""
    pass

    # def testCSV(self):
    #     uri = 'mock://data.cityofnewyork.us/api/views/kku6-nxdu/rows.csv?accessType=DOWNLOAD'
    #     with requests_mock.Mocker() as mock:
    #         mock.get(uri, text=read_file('Demographic Statistics By Zip Code.csv'))
    #         results = datafy.get(uri, request_filesize=False, type_hints=('text/csv', 'csv'))
    #         assert ok(results)
    #         expected = [{'fp': '.', 'mime': 'text/csv', 'ext': 'csv'}]
    #         assert match(results, expected)
    #
    # def testGeoJSON(self):
    #     uri = 'mock://data.cityofnewyork.us/api/geospatial/arq3-7z49?method=export&format=GeoJSON'
    #     with requests_mock.Mocker() as mock:
    #         mock.get(uri, text=read_file('Subway Stations.geojson'))
    #         results = datafy.get(uri, request_filesize=False, type_hints=('text/csv', 'csv'))
    #         assert ok(results)
    #         expected = [{'fp': '.', 'mime': 'text/csv', 'ext': 'csv'}]
    #         assert match(results, expected)
    #
    #     _, _, type = datafy.get(
    #         "https://data.cityofnewyork.us/api/geospatial/arq3-7z49?method=export&format=GeoJSON")[0].values()
    #     assert type == "geojson"
    #
    # def testJSON(self):
    #     _, _, type = datafy.get(
    #         "https://data.cityofnewyork.us/api/views/kku6-nxdu/rows.json?accessType=DOWNLOAD")[0].values()
    #     assert type == "json"
    #
    # def testShapefile(self):
    #     ret = datafy.get("https://data.cityofnewyork.us/api/geospatial/arq3-7z49?method=export&format=Shapefile")
    #     assert len(list(filter(lambda d: d[2] == "shp", ret))) > 0
    #
    # def testZippedExcelFiles(self):
    #     # Plus a Word document.
    #     docs = datafy.get("https://data.cityofnewyork.us/download/gua4-p9wg/application%2Fzip")
    #     filetypes = [t[2] for t in docs]
    #     assert len(list(filter(lambda f: f == 'xlsx', filetypes))) == 7
    #     assert len(list(filter(lambda f: f == 'docx', filetypes))) == 1
    #
    # def testXLSX(self):
    #     _, _, type = datafy.get("https://data.cityofnewyork.us/download/vnwz-ihnf/application%2Fzip")[0].values()
    #     assert type == "xlsx"
