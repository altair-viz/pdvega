# ``pdvega``: Vega-Lite plotting for Pandas Dataframes

[![build status](http://img.shields.io/travis/jakevdp/pdvega/master.svg?style=flat)](https://travis-ci.org/jakevdp/pdvega)

``pdvega`` is a library that allows you to quickly create interactive
[Vega-Lite](https://vega.github.io/vega-lite/) plots from Pandas dataframes,
using an API that is nearly identical to Pandas' built-in
[visualization tools](https://pandas.pydata.org/pandas-docs/stable/visualization.html), and designed for easy use within the [Jupyter notebook](http://jupyter.org).

- [Full Documentation](http://jakevdp.github.io/pdvega/)

Pandas currently has some basic plotting capabilities based on
[matplotlib](http://matplotlib.org). So, for example, you can create
a scatter plot this way:

```python
import numpy as np
import pandas as pd

df = pd.DataFrame({'x': np.random.randn(100), 'y': np.random.randn(100)})
df.plot.scatter(x='x', y='y')
```

![matplotlib scatter output](images/mpl-scatter.png?raw=true)

The goal of ``pdvega`` is that any time you use ``dataframe.plot``, you'll be
able to replace it with ``dataframe.vgplot`` and instead get a similar
(but prettier and more interactive) visualization output in Vega-Lite:

```python
import pdvega  # import adds vgplot attribute to pandas

df.vgplot.scatter(x='x', y='y')
```

![vega-lite scatter output](images/vg-scatter.png?raw=true)

Please see the [Documentation](http://jakevdp.github.io/pdvega/) for a full
set of usage examples.

## Installation

You can get started with ``pdvega`` using pip:

```
$ pip install jupyter pdvega
$ jupyter nbextension install --sys-prefix --py vega3
```

The first line installs ``pdvega`` and its dependencies; the second installs
the Jupyter extensions that allows plots to be displayed in the Jupyter
notebook. For more information on installation and dependencies, see the
[Installation docs](https://jakevdp.github.io/pdvega/installation.html).

## Relationship to Altair

[Altair](http://altair-viz.github.io) is a project that seeks to design an intuitive declarative API for generating Vega-Lite and Vega visualizations, using Pandas dataframes as data sources.

By contrast, ``pdvega`` seeks not to design new visualization APIs, but to use the existing ``DataFrame.plot`` [visualization api](https://pandas.pydata.org/pandas-docs/stable/visualization.html) and output visualizations with Vega/Vega-Lite rather than with matplotlib.

In this respect, ``pdvega`` is quite similar in spirit to the now-defunct [mpld3](http://mpld3.github.io) project, though the scope is smaller and (hopefully) **much** more manageable.
