.. raw :: html

   <a href="https://github.com/jakevdp/pdvega"><img style="position: absolute; top: 0; right: 0; border: 0;" src="https://camo.githubusercontent.com/a6677b08c955af8400f44c6298f40e7d19cc5b2d/68747470733a2f2f73332e616d617a6f6e6177732e636f6d2f6769746875622f726962626f6e732f666f726b6d655f72696768745f677261795f3664366436642e706e67" alt="Fork me on GitHub" data-canonical-src="https://s3.amazonaws.com/github/ribbons/forkme_right_gray_6d6d6d.png"></a>

PdVega: Interactive Vega-Lite Plots for Pandas
==============================================

``pdvega`` is a library that allows you to quickly create interactive
`Vega-Lite`_ plots from Pandas dataframes, using an API that is nearly
identical to Pandas' built-in `plotting API <https://pandas.pydata.org/pandas-docs/stable/visualization.html>`_,
and designed for easy use within the `Jupyter notebook`_.

.. pdvega-plot::

    import pandas as pd
    import numpy as np
    data = pd.DataFrame({'x': np.random.randn(200),
                         'y': np.random.randn(200)})

    import pdvega  # adds vgplot attribute to pandas
    data.vgplot.scatter('x', 'y')

The result is an interactive plot rendered using `Vega-Lite`_, a visualization
specification that allows users to declaratively describe which
data features should map to which visualization features using a well-defined
JSON schema. The result is beautiful and dynamic data visualizations with a
minimum of boiler-plate.

``pdvega`` aims to make the construction of these specifications
more accessible to Python users, via a familiar plotting API.

Quick Start
-----------
``pdvega`` is designed to be used primarily with the `Jupyter notebook`_.
To get started, first install ``pdvega`` with the following commands::

    $ pip install pdvega
    $ jupyter nbextension install --sys-prefix --py vega3

(for details on installation and dependencies, see :ref:`installation`).

With the package installed and imported, you can use the ``vgplot`` attribute
of Pandas ``Series`` and ``DataFrame`` objects to quickly create a Vega-Lite
plot. For convenience here, we will load example datasets using the
`vega_datasets`_ package:

.. pdvega-plot::

    # load a dataframe containing stock price time-series
    from vega_datasets import data
    stocks = data.stocks(pivoted=True)

    # importing pdvega adds the `vgplot` attribute to pandas objects
    import pdvega

    stocks.vgplot.line()

Notice that by default plots created with ``pdvega`` are interactive: you can
use your mouse or track pad to pan and zoom the plot.

By design, ``pdvega`` has a plotting API that is nearly identical to Pandas'
existing `matplotlib API <https://pandas.pydata.org/pandas-docs/stable/visualization.html>`_;
just replace ``data.plot`` with ``data.vgplot``, where
``data`` refers to any Pandas ``Series`` or ``DataFrame`` object:

.. plot::
    :context:
    :nofigs:

    from vega_datasets import data
    stocks = data.stocks(pivoted=True)

.. plot::
    :include-source:
    :context:

    # create a matplotlib line plot
    stocks.plot.line(y='AAPL', alpha=0.5)


.. pdvega-setup::

    from vega_datasets import data
    stocks = data.stocks(pivoted=True)
    import pdvega

.. pdvega-plot::

    # create a vega line plot
    stocks.vgplot.line(y='AAPL', alpha=0.5)

``pdvega`` does not (yet?) support every available argument supported by
``DataFrame.plot`` methods, but it covers the most commonly-used arguments.

To see more examples of visualizations created using the ``vgplot`` attribute
of pandas ``Series`` and ``DataFrame`` objects, see :ref:`core-plotting`.

More Complex Plots
------------------

The ``pdvega`` package additionally supports many of the more sophisticated
plotting routines available in the
`pandas.plotting <https://pandas.pydata.org/pandas-docs/stable/visualization.html#plotting-tools>`_
submodule; for example, here is a multi-panel scatter-plot matrix of Fisher's
`Iris dataset`_:

.. pdvega-setup::

    import pdvega
    from vega_datasets import data

.. pdvega-plot::

    iris = data.iris()
    pdvega.scatter_matrix(iris, 'species', figsize=(7, 7))

In this plot, you can click and drag for linked panning and zooming, or you can
click and drag while holding the SHIFT key to do linked brushing of the points.

For more examples of statistical visualizations available in
``pdvega.plotting``, see :ref:`statistical-plotting`.


Documentation
-------------

.. toctree::
   :maxdepth: 2

   installation
   core
   plotting
   advanced
   API

`pdvega` is MIT-licensed and the source is available on `GitHub <http://github.com/jakevdp/pdvega>`_.
If any questions or issues come up as you use it, please get in touch via
`Git Issues <http://github.com/jakevdp/pdvega/issues>`_.

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. _Vega-Lite: http://vega.github.io/vega-lite
.. _Jupyter notebook: http://jupyter.org/
.. _vega_datasets: http://github.com/jakevdp/vega_datasets
.. _Iris dataset: https://en.wikipedia.org/wiki/Iris_flower_data_set
