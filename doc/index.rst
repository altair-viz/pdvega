PdVega: Interactive Vega Plots for Pandas
=========================================

``pdvega`` is a library that allows you to quickly create interactive
`Vega-Lite`_ plots from Pandas dataframes, using an API that is nearly
identical to Pandas' built-in `matplotlib plotting API <https://pandas.pydata.org/pandas-docs/stable/visualization.html>`_, and designed for easy use
within the `Jupyter notebook`_.

Quick Start
-----------
To get started with ``pdvega``, run the following installation commands:

.. code-block:: bash

    $ pip install pdvega
    $ jupyter nbextension install --sys-prefix --py vega3

(for details on installation and dependencies, see :ref:`installation`).

With the package installed, you can use the ``vgplot`` attribute of Pandas
objects to quickly create a Vega-Lite plot (for convenience, we load an
example dataframe using the `vega_datasets`_ package):

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
existing matplotlib API; just replace ``data.plot`` with ``data.vgplot``, where
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
``DataFrame.plot`` methods, but it covers the most commonly-used ones.

To see more examples of visualizations created using the ``vgplot`` attribute
of pandas ``Series`` and ``DataFrame`` objects, see :ref:`core-plotting`.

Statistical Plots
-----------------

The ``pdvega`` package additionally supports many of the more sophisticated
statistical visualization routines available in ``pandas.plotting``;
for example, here is a multi-panel scatter-plot matrix of the well-known
iris dataset

.. pdvega-setup::

    import pdvega
    from vega_datasets import data

.. pdvega-plot::

    iris = data.iris()
    pdvega.scatter_matrix(iris, 'species', figsize=(8, 8))

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


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. _Vega-Lite: http://vega.github.io/vega-lite
.. _Jupyter notebook: http://jupyter.org/
.. _vega_datasets: http://github.com/jakevdp/vega_datasets
