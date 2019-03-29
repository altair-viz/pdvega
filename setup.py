import io
import os
import re

from setuptools import setup


def read(path, encoding='utf-8'):
    path = os.path.join(os.path.dirname(__file__), path)
    with io.open(path, encoding=encoding) as fp:
        return fp.read()


def get_install_requirements(path):
    content = read(path)
    return [
        req
        for req in content.split("\n")
        if req != '' and not req.startswith('#')
    ]


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


HERE = os.path.abspath(os.path.dirname(__file__))

# From https://github.com/jupyterlab/jupyterlab/blob/master/setupbase.py, BSD licensed
def find_packages(top=HERE):
    """
    Find all of the packages.
    """
    packages = []
    for d, dirs, _ in os.walk(top, followlinks=True):
        if os.path.exists(os.path.join(d, '__init__.py')):
            packages.append(os.path.relpath(d, top).replace(os.path.sep, '.'))
        elif d != top:
            # Do not look for packages in subfolders if current is not a package
            dirs[:] = []
    return packages


DESCRIPTION = "Pandas plotting interface to Vega and Vega-Lite"
LONG_DESCRIPTION = """
pdvega makes it easy to create Vega-Lite plots from pandas dataframes,
using the familiar pandas visualization API. For more information, see
the `pdvega documentation <http://altair-viz.github.io/pdvega/>`_.
"""
NAME = "pdvega"
AUTHOR = "Jake VanderPlas"
AUTHOR_EMAIL = "jakevdp@gmail.com"
MAINTAINER = "Jake VanderPlas"
MAINTAINER_EMAIL = "jakevdp@gmail.com"
URL = 'http://altair-viz.github.io/pdvega/'
DOWNLOAD_URL = 'http://github.com/altair-viz/pdvega/'
LICENSE = 'MIT'
INSTALL_REQUIRES = get_install_requirements("requirements.txt")
DEV_REQUIRES  = get_install_requirements("requirements_dev.txt")
PACKAGES = find_packages()
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
      install_requires=INSTALL_REQUIRES,
      extras_require={
        'dev': DEV_REQUIRES
      },
      packages=PACKAGES,
      include_package_data=True,
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
