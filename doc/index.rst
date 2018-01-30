PdVega: Interactive Vega Plots for Pandas
=========================================

``pdvega`` is a library that allows you to quickly create interactive
`Vega-Lite`_ plots from Pandas dataframes, using an API that is nearly
identical to Pandas' built-in matplotlib plotting API.


Example
-------
Here is an example of using the Altair API to quickly visualize a dataset:

.. pdvega-plot::

    import pdvega
    from vega_datasets import data

    stocks = data.stocks(pivoted=True)
    stocks.vgplot()

Notice that by default the plot is interactive; it is pannable and zoomable.

PdVega supports even more complicated plots as well:

.. pdvega-plot::

    import pdvega
    from vega_datasets import data

    iris = data.iris()
    pdvega.scatter_matrix(iris, 'species', figsize=(8, 8))

In this plot, you can click and drag for linked panning and zooming, or you can
click and drag while holding the SHIFT key to do linked brushing.


Documentation
-------------

.. toctree::
   :maxdepth: 2


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. _Vega-Lite: http://vega.github.io/vega-lite
