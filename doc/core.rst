.. _core-plotting:

Simple Visualizations with ``data.vgplot``
==========================================

The core interface of ``pdvega`` is the ``vgplot`` attribute that it adds to
Pandas ``DataFrame`` and ``Series`` objects::

    import pdvega

.. pdvega-setup::

   import pdvega

   from vega_datasets import data
   iris = data.iris()

Like the ``plot`` attribute that is built-in to Pandas, there are two ways of
creating plots with ``vgplot``: first, you can call the ``vgplot`` attribute
of a Pandas object directly:

.. pdvega-plot::

   from vega_datasets import data
   iris = data.iris()

   iris.vgplot(kind='scatter', x='sepalLength', y='petalLength', c='species')

Equivalently, you can call the specific method associated with each plot type:

.. pdvega-plot::

   iris.vgplot.scatter(x='sepalLength', y='petalLength', c='species')

The benefit of the second approach is that it allows exploration of available
plot types via tab completion, and the individual functions also provide more
detailed documentation of the arguments available for each method.

The ``vgplot`` interface exposes nine basic plot types; we will show examples
of these below.

Datasets
--------
For the examples on this page, we will use a number of datasets made available
in the `vega_datasets`_ package:

.. pdvega-setup::
   :show:

   iris = data.iris()
   stocks = data.stocks(pivoted=True)
   cars = data.cars()

These datasets are stored in the form of pandas dataframes::

     >>> iris.head()
        petalLength  petalWidth  sepalLength  sepalWidth species
     0          1.4         0.2          5.1         3.5  setosa
     1          1.4         0.2          4.9         3.0  setosa
     2          1.3         0.2          4.7         3.2  setosa
     3          1.5         0.2          4.6         3.1  setosa
     4          1.4         0.2          5.0         3.6  setosa

     >>> stocks.head()
     symbol       AAPL   AMZN  GOOG     IBM   MSFT
     date
     2000-01-01  25.94  64.56   NaN  100.52  39.81
     2000-02-01  28.66  68.87   NaN   92.11  36.35
     2000-03-01  33.95  67.00   NaN  106.11  43.22
     2000-04-01  31.01  55.19   NaN   99.95  28.37
     2000-05-01  21.00  48.31   NaN   96.31  25.45


     >>> cars.head()
        Acceleration  Cylinders  Displacement  Horsepower  Miles_per_Gallon  \
     0          12.0          8         307.0       130.0              18.0
     1          11.5          8         350.0       165.0              15.0
     2          11.0          8         318.0       150.0              18.0
     3          12.0          8         304.0       150.0              16.0
     4          10.5          8         302.0       140.0              17.0

                             Name Origin  Weight_in_lbs        Year
     0  chevrolet chevelle malibu    USA           3504  1970-01-01
     1          buick skylark 320    USA           3693  1970-01-01
     2         plymouth satellite    USA           3436  1970-01-01
     3              amc rebel sst    USA           3433  1970-01-01
     4                ford torino    USA           3449  1970-01-01

.. _vgplot-line:

Line Plots with ``vgplot.line``
-------------------------------
The default plot type for ``vgplot`` is a line plot:

.. pdvega-plot::

   stocks.vgplot()

Unless otherwise specified, the index of the DataFrame or series is used as the
x-axis variable, and a separate line will be created for the y-values in each
column in the dataframe. If you'd like to plot a subset of the columns, you can use
pandas indexing to select the columns you are interested in:

.. pdvega-plot::

   stocks[['AAPL', 'AMZN']].vgplot.line()

Optionally, you can specify the column names to use for the x-axis and y-axis:

.. pdvega-plot::

  stocks.vgplot.line(x='AAPL', y='AMZN')

Line plots can be further customized; see the function documentation for
more information:

- Series line plot: :meth:`pdvega.SeriesPlotMethods.line`
- DataFrame line plot: :meth:`pdvega.FramePlotMethods.line`

.. _vgplot-scatter:

Scatter Plots with ``vgplot.scatter``
-------------------------------------
The previous plot might make more sense in the form of a scatter plot.
This can be done with ``vgplot.scatter()``:

.. pdvega-plot::

    stocks.vgplot.scatter(x='AAPL', y='AMZN')

You can also encode the color and size of scatter plots; let's switch to the
cars dataset to see the relationship between some of these variables:

.. pdvega-plot::

    cars.vgplot.scatter(x='Horsepower', y='Miles_per_Gallon',
                        c='Origin', s='Weight_in_lbs', alpha=0.5)

This is one slight difference from the Pandas plot interface: in Pandas the
``c`` and ``s`` parameters must be passed as arrays, while here we pass them
as column names.

Scatter plots can be further customized; see :meth:`pdvega.FramePlotMethods.scatter`
for more information.

.. _vgplot-area:

Area Plots with ``vgplot.area``
-------------------------------
Area plots are quite similar to line plots, but curves are filled and stacked,
meaning the top curve reflects the sum of all the ones below:

.. pdvega-plot::

   stocks[['MSFT', 'AAPL', 'AMZN']].vgplot.area()


Area charts can also be unstacked and overlaid, in which case transparency
can be useful:

.. pdvega-plot::

   stocks[['MSFT', 'AAPL', 'AMZN']].vgplot.area(stacked=False, alpha=0.4)

Area plots can be further customized; see the function documentation for
more information:

- Series area plot: :meth:`pdvega.SeriesPlotMethods.area`
- DataFrame area plot: :meth:`pdvega.FramePlotMethods.area`

.. _vgplot-bar:

Bar Charts with ``vgplot.bar``
------------------------------

Bar charts are supported using ``vgplot.bar()``. Let's create a small dataset
to use for this:

.. pdvega-setup::
   :show:

   import numpy as np
   import pandas as pd
   np.random.seed(1234)

   df = pd.DataFrame(np.random.rand(10, 2), columns=['a', 'b'])

.. pdvega-plot::

   df.vgplot.bar()

Multiple bar plots will be layered on top of each other; like with area charts,
they can be stacked using the ``stacked=True`` option:

.. pdvega-plot::

   df.vgplot.bar(stacked=True)

Additionally, horizontal bar plots can be created with ``barh``:

.. pdvega-plot::

   df.vgplot.barh(stacked=True)

Bar charts can be further customized; see the function documentation for
more information:

- Series bar plots: :meth:`pdvega.SeriesPlotMethods.bar`, :meth:`pdvega.SeriesPlotMethods.barh`
- DataFrame bar plots: :meth:`pdvega.FramePlotMethods.bar`, :meth:`pdvega.FramePlotMethods.barh`


.. _vgplot-hist:

Histograms with ``vgplot.hist``
-------------------------------
Histograms can be created with the ``vgplot.hist()`` method.

Let's create some data to make some distributions:

.. pdvega-setup::
   :show:

   import pandas as pd
   import numpy as np
   df = pd.DataFrame({'a': np.random.randn(1000) + 1,
                      'b': np.random.randn(1000),
                      'c': np.random.randn(1000) - 1},
                     columns=['a', 'b', 'c'])

We'll specify 50 bins, and create a layered histogram with a 50% transparency:

.. pdvega-plot::

   df.vgplot.hist(bins=50, alpha=0.5)

Alternatively, we can stack the histogram, and use ``histtype`` to specify that
we want a filled step chart rather than a bar chart:

.. pdvega-plot::

   df.vgplot.hist(histtype='stepfilled', stacked=True, bins=50)

Histograms can be further customized; see the function documentation for
more information:

- Series histogram: :meth:`pdvega.SeriesPlotMethods.hist`
- DataFrame histogram: :meth:`pdvega.FramePlotMethods.hist`

.. _vgplot-kde:

KDE/Density plots with ``vgplot.kde``
-------------------------------------
Similar to a histogram is a kernel density estimation plot (kde) which creates
a smooth curve representing the density of points. This can be created with
the ``vgplot.kde`` method. We'll use the same data we did in the histogram
section:

.. pdvega-plot::

   df.vgplot.kde()

KDE plots can be further customized; see the function documentation for
more information:

- Series kde plots: :meth:`pdvega.SeriesPlotMethods.kde`
- DataFrame kde plots: :meth:`pdvega.FramePlotMethods.kde`


.. _vgplot-pie-chart:

Pie Charts
----------
No.

.. _vgplot-heatmap:

Heatmaps
--------
Pandas plotting has a function to create a hexagonally-binned heatmap of
two-dimensional data. Unfortunately neither Vega nor Vega-Lite currently
support hexagonal binning. But they do support cartesian heatmaps, and this
functionality is included in ``pdvega``:

.. pdvega-plot::

   df.vgplot.heatmap(x='a', y='b', gridsize=20)

Here the ``gridsize`` parameter indicates approximately how many grid points
span the plot. Alternatively, instead of computing the count within each bin,
we can compute the mean of a third column, specified by the ``C`` parameter:

.. pdvega-plot::

   df.vgplot.heatmap(x='a', y='b', C='c', gridsize=20)


Heatmap plots can be further customized; see :meth:`pdvega.FramePlotMethods.heatmap`
for more information.

Other Plot Types
----------------
The above plots are the basic plot types supported by ``pdvega``; more sophisticated
plots are available in the :mod:`pdvega.plotting` module.
For examples of these, refer to :ref:`statistical-plotting`.



.. _vega_datasets: http://github.com/jakevdp/vega_datasets
