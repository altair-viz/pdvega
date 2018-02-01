import io
import os
import re

from setuptools import setup


def read(path, encoding='utf-8'):
    path = os.path.join(os.path.dirname(__file__), path)
    with io.open(path, encoding=encoding) as fp:
        return fp.read()


def version(path):
    """Obtain the packge version from a python file e.g. pkg/__init__.py
    See <https://packaging.python.org/en/latest/single_source_version.html>.
    """
    version_file = read(path)
    version_match = re.search(r"""^__version__ = ['"]([^'"]*)['"]""",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


DESCRIPTION = "Pandas plotting interface to Vega and Vega-Lite"
LONG_DESCRIPTION = """
pdvega makes it easy to create Vega-Lite plots from pandas dataframes,
using the familiar pandas visualization API. For more information, see
the `pdvega documentation <http://jakevdp.github.io/pdvega/>`_.
"""
NAME = "pdvega"
AUTHOR = "Jake VanderPlas"
AUTHOR_EMAIL = "jakevdp@gmail.com"
MAINTAINER = "Jake VanderPlas"
MAINTAINER_EMAIL = "jakevdp@gmail.com"
URL = 'http://jakevdp.github.io/pdvega/'
DOWNLOAD_URL = 'http://github.com/jakevdp/pdvega/'
LICENSE = 'MIT'

VERSION = version('pdvega/__init__.py')

setup(name=NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      maintainer=MAINTAINER,
      maintainer_email=MAINTAINER_EMAIL,
      url=URL,
      download_url=DOWNLOAD_URL,
      license=LICENSE,
      install_requires=["pandas", "vega3", "ipython"],
      tests_require=["pytest", "jsonschema"],
      packages=['pdvega', 'pdvega.tests'],
      package_data={'pdvega': ['*.json']},
      classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'],
     )
