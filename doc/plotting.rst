.. _statistical-plotting:

Statistical Visualization with ``pdvega.plotting``
==================================================

In addition to the basic plots made available by the ``vgplot`` interface,
``pdvega.plotting`` makes available some more sophisticated plotting types
that mirror those available in `pandas.plotting`_.

This section will outline a few of these.

.. pdvega-setup::

   import pdvega
   from vega_datasets import data
   iris = data.iris()
   stocks = data.stocks(pivoted=True)

.. _pdvega-scatter-matrix:

Scatter Matrix
--------------

For multi-dimensional data, it is difficult to capture all the relevant data
features using a simple scatter plot. For data with several attributes, it can
be useful to visualize the pairwise relationships between all pairs of dimensions.
This is done by ``pdvega.scatter_matrix``, which has an API based on
:func:`pandas.plotting.scatter_matrix`:

.. pdvega-plot::

   pdvega.scatter_matrix(iris, "species", figsize=(7, 7))

Notice that this version is interactive in two ways: if you click and drag on
any frame of the plot, all frames scales are dynamically adjusted in concert.
Further, if you hold the SHIFT key while clicking and dragging, it enables a
linked-brushing operation that allows you to track points between panels.


.. _pdvega-parallel-coordinates:

Parallel Coordinates
--------------------

Another way to visualize multi-dimensional data is to look at each dimension
independently, using a *parallel coordinates* plot. This can be done using
:func:`pdvega.parallel_coordinates`, which follows the API of
:func:`pandas.plotting.parallel_coordinates`:

.. pdvega-plot::

   pdvega.parallel_coordinates(iris, "species")

In one glance, this lets you see relationships between points, and in particular
makes clear that the "setosa" species is well-separated from the other two
in the dimensions of petal width and length.

.. _pdvega-andrews-curves:

Andrews Curves
--------------

A similar approach to visualizing data dimensions is known as *Andrews curves*:
the idea is to construct a Fourier series from the features of each object,
in order to qualitatively visualize the aggregate differences between classes.
This can be done with the :func:`pdvega.andrews_curves` function, which follows
the API of :func:`pandas.plotting.andrews_curves`:

.. pdvega-plot::

   pdvega.andrews_curves(iris, "species")

This gives us a similar impression to what we saw in the parallel coordinates
plot -- that setosa is somehow distinct from the other species -- but gives
less quantitative insight into just which features lead to that distinction.

.. _pdvega-lag-plot:

Lag Plot
--------

Finally, for time series, an interesting type of plot is known as a *lag plot*.
This is implemented by the :func:`pdvega.plotting.lag_plot` function, which follows
the API of :func:`pandas.plotting.lag_plot`.

Here we'll visualize the stock prices of Amazon and Microsoft from 1998-2010,
using a lag of 12 months:

.. pdvega-plot::

   pdvega.lag_plot(stocks[['AMZN', 'MSFT']], lag=12)

It's immediately apparent from this plot that Amazon was far more volitile
during that period: its price at any point during this period showed very
little correlation with the price a year later. By contrast, it's clear that
Microsoft's price was much more stable through this decade.

We can see that interpretation as well in the simple time-series plot of each
company's stock price:

.. pdvega-plot::

   stocks[['AMZN', 'MSFT']].vgplot.line()



.. _pandas.plotting: http://pandas.pydata.org/
