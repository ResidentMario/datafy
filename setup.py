from setuptools import setup
setup(
    name = 'datafy',
    packages = ['datafy'], # this must be the same as the name above
    install_requires=['pandas', 'geopandas', 'requests', 'requests-file'],
    py_modules=['datafy'],
    version = '0.0.1',
    description = 'Read download URLs into datasets.',
    author = 'Aleksey Bilogur',
    author_email = 'aleksey.bilogur@gmail.com',
    url = 'https://github.com/ResidentMario/datafy',
    download_url = 'https://github.com/ResidentMario/datafy/tarball/0.0.1',
    keywords = ['data', 'requests', 'data analysis', 'geospatial data', 'geospatial analytics', 'pandas'],
    classifiers = [],
)