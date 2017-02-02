import pandas as pd
import geopandas as gpd
import requests
import mimetypes
import io
import zipfile
import os
import random
import shutil
from requests_file import FileAdapter


mime_map = {
    'text/csv': 'csv',
    'application/geo+json': 'geojson',
    'application/vnd.geo+json': 'geojson',  # Obselete, but used by Socrata as of 1/23/2017
    'application/vnd.google-earth.kmz': 'kmz',
    'application/vnd.google-earth.kml+xml': 'kml',
    'application/zip': 'zip',
    'application/json': 'json',
    'application/xml': 'xml',
    'text/xml': 'xml',
}


# Set up requests so that it can be used inline with local files.
requests_session = requests.Session()
requests_session.mount("file://", FileAdapter())


def get(uri, sizeout=1000, type=None, encoding=None):

    # First send a HEAD request and back out if sizeout is exceeded. Don't do this if the file is local.
    if "file://" not in uri:
        try:
            # Note: requests uses case-insenitive header names for access purposes. Saves a headache.
            content_length = requests.head(uri, timeout=1).headers['content-length']
            if content_length > sizeout:
                return None
        except KeyError:
            pass

    # Then send a GET request.
    r = requests_session.get(uri, timeout=7)

    # Get the content type and encoding from the header. e.g. "text/csv; encoding=utf-8" => (csv, utf-8)
    # Note that file-magic and python-magic modules exist for this, but are UNIX dependent because they rely on the
    # native libmagic library. Getting that running on Windows would require a lot of effort. For now, let's see if
    # we can maintain portability. That may ultimately be a mistake.
    #
    # All of the vendors that have to ascertain MIME types (including python-magic) uses a variety of lists to do it,
    # backed up by inspection heuristics for when the hard-coded lists fail.
    #
    # We only want to accept a handful of MIME types (http://www.iana.org/assignments/media-types/media-types.xhtml)
    # from the full list, and we assume that the open data portals hosting these services are competent enough to
    # send their data with the correct content types. I built this into the list above this method signature.
    #
    # If we absolutely must use an oracle, we can drop that in here later.
    if type:
        type_hint = type
        encoding_hint = encoding
    else:
        split = r.headers['content-type'].split()

        # First try our guess.
        try:
            type_hint = mime_map[split[0]]
        except KeyError:
            type_hint = None

        # Then try to use Python's built-in mimetypes module to classify.
        if not type_hint:
            try:
                type_hint = mimetypes.guess_extension(split[0].rstrip(";"))[1:]
            except TypeError:
                type_hint = None

        # Raise if neither method works.
        if not type_hint:
            raise IOError("Couldn't determine meaning of content-type {0} associated with the URI {1}".format(
                type_hint, uri
            ))

        # Get the encoding hint, if there is one.
        encoding_hint = split[1].replace("charset=", "") if len(split) > 1 else None

    # If the URI contains a "file://" in front, we know that this piece of data was read out of an archival file format.
    # In that case, we need to pull in a filepath hint so that we can point to which specific file in the resource is
    # the dataset of interest. Otherwise, the entire resource is itself the dataset of interest, and we denote the path
    # with a ".".
    filepath_hint = uri.replace("file://", "") if "file://" in uri else "."

    # Use the hints to load the data.
    if type_hint == "csv":
        return [(pd.read_csv(io.BytesIO(r.content), encoding=encoding_hint), filepath_hint, type_hint)]
    elif type_hint == "geojson":
        data = gpd.GeoDataFrame(r.json())
        return [(data, filepath_hint, type_hint)]

    # We assume that JSON data gets passed with a JSON content-type and GeoJSON with a GeoJSON content-type. This is
    # true of the Socrata open data portal, and *probably* true of other open data portal providers, but a rule that is
    # almost certainly broken by less well-behaved landing pages on the net. For those cases, use the type parameter
    # over-ride.
    elif type_hint == "json":
        data = r.json()
        return [(data, filepath_hint, type_hint)]

    elif type_hint == "xls":
        data = pd.read_excel(io.BytesIO(r.content), encoding=encoding_hint)
        return [(data, filepath_hint, type_hint)]

    elif type_hint == "zip":
        # In certain cases, it's possible to the contents of an archive virtually. This depends on the contents of the
        # file: shapefiles can't be read because they are split across multiple files, KML and KMZ files can't be read
        # because fiona doesn't support them. But most of the rest of things can be.
        #
        # To keep the API simple, however, we're not going to do the three-way fork required to do this. Instead we're
        # going to take the performance hit of writing to disk in all cases (which is really trivial anyway compared to
        # the cost of downloading), and analyze that in-place.
        #
        # This branch will then recursively call get as a subroutine, using the file driver to pick out the rest of the
        # files in the folder.
        z = zipfile.ZipFile(io.BytesIO(r.content))
        while True:
            temp_foldername = str(random.randint(0, 1000000))  # minimize the chance of a collision
            if not os.path.exists(temp_foldername):
                os.makedirs(temp_foldername)
                break
        z.extractall(path=temp_foldername)

        # Recuse using the file driver to deal with local folders.
        ret = []
        for filename in z.namelist():
            type = filename.split(".")[-1]
            ret += get("file:///{0}/{1}".format(temp_foldername, filename), type=type)

        # Delete the folder before returning the data.
        shutil.rmtree(temp_foldername)
        return ret

    elif type_hint == "shp":
        # This will only happen on a file read, because shapefiles can't be a content-type on the web.
        data = gpd.read_file(uri.replace("file:///", ""))
        return [(data, filepath_hint, type_hint)]

    else:
        # We ignore file formats we don't know how to deal with as well as shapefile support files handled elsewhere.
        return [(None, filepath_hint, type_hint)]