import numpy as np
import pandas as pd

from ._utils import (infer_vegalite_type, finalize_vegalite_spec,
                     unpivot_frame, warn_if_keywords_unused)
from ._pandas_internals import (PandasObject,
                                register_dataframe_accessor,
                                register_series_accessor)

from ._axes import Axes


class BasePlotMethods(PandasObject):
    def __init__(self, data):
        self._data = data

    def __call__(self, kind, *args, **kwargs):
        raise NotImplementedError()


@register_series_accessor('vgplot')
class SeriesPlotMethods(BasePlotMethods):
    """Series Accessor & Method for creating Vega-Lite visualizations.

    Examples
    --------
    >>> s.vgplot.line()  # doctest: +SKIP
    >>> s.vgplot.area()  # doctest: +SKIP
    >>> s.vgplot.bar()  # doctest: +SKIP
    >>> s.vgplot.barh()  # doctest: +SKIP
    >>> s.vgplot.hist()  # doctest: +SKIP
    >>> s.vgplot.kde()  # doctest: +SKIP
    >>> s.vgplot.density()  # doctest: +SKIP

    Plotting methods can also be accessed by calling the accessor as a method
    with the ``kind`` argument: ``s.vgplot(kind='line', **kwds)``
    is equivalent to ``s.vgplot.line(**kwds)``
    """
    def __call__(self, kind='line', **kwargs):
        try:
            plot_method = getattr(self, kind)
        except AttributeError:
            raise ValueError("kind='{0}' not valid for {1}"
                             "".format(kind, self.__class__.__name__))
        return plot_method(**kwargs)

    def line(self, alpha=None, interactive=True, width=450, height=300, **kwds):
        """Line plot for Series data

        >>> series.vgplot.line()  # doctest: +SKIP

        Parameters
        ----------
        alpha : float, optional
            transparency level, 0 <= alpha <= 1
        interactive : bool, optional
            if True (default) then produce an interactive plot
        width : int, optional
            the width of the plot in pixels
        height : int, optional
            the height of the plot in pixels

        Returns
        -------
        axes : pdvega.Axes
            The vega-lite plot
        """
        warn_if_keywords_unused('line', kwds)
        data = self._data
        df = data.reset_index()
        df.columns = map(str, df.columns)
        x, y = df.columns

        spec = {
          "mark": "line",
          "encoding": {
            "x": {
                "field": x,
                "type": infer_vegalite_type(df[x], ordinal_threshold=0)
            },
            "y": {
                "field": y,
                "type": infer_vegalite_type(df[y], ordinal_threshold=0)
            },
          }
        }

        if alpha is not None:
            assert 0 <= alpha <= 1
            spec['encoding']['opacity'] = {'value': alpha}

        spec = finalize_vegalite_spec(spec, interactive=interactive,
                                      width=width, height=height)
        return Axes(spec, data=df)

    def area(self, alpha=None, interactive=True, width=450, height=300, **kwds):
        """Area plot for Series data

        >>> series.vgplot.area()  # doctest: +SKIP

        Parameters
        ----------
        alpha : float, optional
            transparency level, 0 <= alpha <= 1
        interactive : bool, optional
            if True (default) then produce an interactive plot
        width : int, optional
            the width of the plot in pixels
        height : int, optional
            the height of the plot in pixels

        Returns
        -------
        axes : pdvega.Axes
            The vega-lite plot
        """
        warn_if_keywords_unused('area', kwds)
        df = self._data.reset_index()
        df.columns = map(str, df.columns)
        x, y = df.columns

        spec = {
          "mark": "area",
          "encoding": {
            "x": {
                "field": x,
                "type": infer_vegalite_type(df[x], ordinal_threshold=0)
            },
            "y": {
                "field": y,
                "type": infer_vegalite_type(df[y], ordinal_threshold=0)
            },
          },
        }

        if alpha is not None:
            assert 0 <= alpha <= 1
            spec['encoding']['opacity'] = {'value': alpha}

        spec = finalize_vegalite_spec(spec, interactive=interactive,
                                      width=width, height=height)
        return Axes(spec, data=df)

    def bar(self, alpha=None, interactive=True,
            width=450, height=300, **kwds):
        """Bar plot for Series data

        >>> series.vgplot.bar()  # doctest: +SKIP

        Parameters
        ----------
        alpha : float, optional
            transparency level, 0 <= alpha <= 1
        interactive : bool, optional
            if True (default) then produce an interactive plot
        width : int, optional
            the width of the plot in pixels
        height : int, optional
            the height of the plot in pixels

        Returns
        -------
        axes : pdvega.Axes
            The vega-lite plot
        """
        warn_if_keywords_unused('bar', kwds)

        df = self._data.reset_index()
        df.columns = map(str, df.columns)
        x, y = df.columns

        spec = {
          "mark": "bar",
          "encoding": {
            "x": {
                "field": x,
                "type": infer_vegalite_type(df[x], ordinal_threshold=50)
            },
            "y": {
                "field": y,
                "type": infer_vegalite_type(df[y], ordinal_threshold=0)
            },
          },
        }

        if alpha is not None:
            assert 0 <= alpha <= 1
            spec['encoding']['opacity'] = {'value': alpha}

        spec = finalize_vegalite_spec(spec, interactive=interactive,
                                      width=width, height=height)
        return Axes(spec, data=df)

    def barh(self, alpha=None, interactive=True,
             width=450, height=300, **kwds):
        """Horizontal bar plot for Series data

        >>> series.vgplot.barh()  # doctest: +SKIP

        Parameters
        ----------
        alpha : float, optional
            transparency level, 0 <= alpha <= 1
        interactive : bool, optional
            if True (default) then produce an interactive plot
        width : int, optional
            the width of the plot in pixels
        height : int, optional
            the height of the plot in pixels

        Returns
        -------
        axes : pdvega.Axes
            The vega-lite plot
        """
        plot = self.bar(alpha=alpha, interactive=interactive,
                        width=width, height=height, **kwds)
        enc = plot.spec['encoding']
        enc['x'], enc['y'] = enc['y'], enc['x']
        return plot

    def hist(self, bins=10, alpha=None, histtype='bar',
             interactive=True, width=450, height=300, **kwds):
        """Histogram plot for Series data

        >>> series.vgplot.hist()  # doctest: +SKIP

        Parameters
        ----------
        bins : integer, optional
            the maximum number of bins to use for the histogram (default: 10)
        alpha : float, optional
            transparency level, 0 <= alpha <= 1
        histtype : string, {'bar', 'step', 'stepfilled'}
            The type of histogram to generate. Default is 'bar'.
        interactive : bool, optional
            if True (default) then produce an interactive plot
        width : int, optional
            the width of the plot in pixels
        height : int, optional
            the height of the plot in pixels

        Returns
        -------
        axes : pdvega.Axes
            The vega-lite plot
        """
        warn_if_keywords_unused('hist', kwds)
        df = self._data.to_frame()
        df.columns = map(str, df.columns)

        if histtype in ['bar', 'barstacked']:
            mark = 'bar'
        elif histtype == 'stepfilled':
            mark = {'type': 'area', 'interpolate': 'step'}
        elif histtype == 'step':
            mark = {'type': 'line', 'interpolate': 'step'}
        else:
            raise ValueError("histtype '{0}' is not recognized"
                             "".format(histtype))

        spec = {
            "mark": mark,
            "encoding": {
                "x": {
                    "bin": {"maxbins": bins},
                    "field": df.columns[0],
                    "type": "quantitative"
                },
                "y": {
                    "aggregate": "count",
                    "type": "quantitative"
                }
            },
        }

        if alpha is not None:
            assert 0 <= alpha <= 1
            spec['encoding']['opacity'] = {'value': alpha}

        spec = finalize_vegalite_spec(spec, interactive=interactive,
                                      width=width, height=height)
        return Axes(spec, data=df)

    def kde(self, bw_method=None, alpha=None,
            interactive=True, width=450, height=300, **kwds):
        """Kernel Density Estimation plot for Series data

        >>> series.vgplot.kde()  # doctest: +SKIP

        Parameters
        ----------
        bw_method : str, scalar or callable, optional
            The method used to calculate the estimator bandwidth. This can be
            'scott', 'silverman', a scalar constant or a callable.
            See `scipy.stats.gaussian_kde` for more details.
        alpha : float, optional
            transparency level, 0 <= alpha <= 1
        interactive : bool, optional
            if True (default) then produce an interactive plot
        width : int, optional
            the width of the plot in pixels
        height : int, optional
            the height of the plot in pixels

        Returns
        -------
        axes : pdvega.Axes
            The vega-lite plot
        """
        from scipy.stats import gaussian_kde

        data = self._data
        tmin, tmax = data.min(), data.max()
        trange = tmax - tmin
        t = np.linspace(tmin - 0.5 * trange, tmax + 0.5 * trange, 1000)

        kde_ser = pd.Series(gaussian_kde(data, bw_method=bw_method).evaluate(t),
                            index=t, name=data.name)
        kde_ser.index.name = ' '
        f = self.__class__(kde_ser)
        return f.line(alpha=alpha, interactive=interactive,
                      width=width, height=height, **kwds)

    density = kde


@register_dataframe_accessor('vgplot')
class FramePlotMethods(BasePlotMethods):
    """DataFrame Accessor & Method for creating Vega-Lite visualizations.

    Examples
    --------
    >>> df.vgplot.line()  # doctest: +SKIP
    >>> df.vgplot.area()  # doctest: +SKIP
    >>> df.vgplot.bar()  # doctest: +SKIP
    >>> df.vgplot.barh()  # doctest: +SKIP
    >>> df.vgplot.hist()  # doctest: +SKIP
    >>> df.vgplot.kde()  # doctest: +SKIP
    >>> df.vgplot.density()  # doctest: +SKIP
    >>> df.vgplot.scatter(x, y)  # doctest: +SKIP
    >>> df.vgplot.hexbin(x, y)  # doctest: +SKIP

    Plotting methods can also be accessed by calling the accessor as a method
    with the ``kind`` argument: ``df.vgplot(kind='line', **kwds)``
    is equivalent to ``df.vgplot.line(**kwds)``
    """
    def __call__(self, x=None, y=None, kind='line', **kwargs):
        try:
            plot_method = getattr(self, kind)
        except AttributeError:
            raise ValueError("kind='{0}' not valid for {1}"
                             "".format(kind, self.__class__.__name__))
        return plot_method(x=x, y=y, **kwargs)

    def line(self, x=None, y=None, alpha=None,
             var_name='variable', value_name='value',
             interactive=True, width=450, height=300, **kwds):
        """Line plot for DataFrame data

        >>> dataframe.vgplot.line()  # doctest: +SKIP

        Parameters
        ----------
        x : string, optional
            the column to use as the x-axis variable. If not specified, the
            index will be used.
        y : string, optional
            the column to use as the y-axis variable. If not specified, all
            columns (except x if specified) will be used.
        alpha : float, optional
            transparency level, 0 <= alpha <= 1
        var_name : string, optional
            the legend title
        value_name : string, optional
            the y-axis label
        interactive : bool, optional
            if True (default) then produce an interactive plot
        width : int, optional
            the width of the plot in pixels
        height : int, optional
            the height of the plot in pixels

        Returns
        -------
        axes : pdvega.Axes
            The vega-lite plot
        """
        warn_if_keywords_unused('line', kwds)
        use_order = (x is not None)

        if use_order:
            df = self._data.reset_index()
            order = df.columns[0]
            df = unpivot_frame(df, x=(x, order), y=y,
                               var_name=var_name, value_name=value_name)
        else:
            df = unpivot_frame(self._data, x=x, y=y,
                               var_name=var_name, value_name=value_name)
            x = df.columns[0]

        spec = {
            "mark": "line",
            "encoding": {
                "x": {
                    "field": x,
                    "type": infer_vegalite_type(df[x],
                                                ordinal_threshold=0)
                },
                "y": {
                    "field": value_name,
                    "type": infer_vegalite_type(df[value_name],
                                                ordinal_threshold=0)
                },
                "color": {
                    "field": var_name,
                    "type": infer_vegalite_type(df[var_name],
                                                ordinal_threshold=10)
                },
            },
        }
        if use_order:
            spec['encoding']['order'] = {
                'field': order,
                'type': infer_vegalite_type(df[order])
            }

        if alpha is not None:
            assert 0 <= alpha <= 1
            spec['encoding']['opacity'] = {'value': alpha}

        spec = finalize_vegalite_spec(spec, interactive=interactive,
                                      width=width, height=height)
        return Axes(spec, data=df)

    def scatter(self, x, y, c=None, s=None, alpha=None,
                interactive=True, width=450, height=300, **kwds):
        """Scatter plot for DataFrame data

        >>> dataframe.vgplot.scatter(x, y)  # doctest: +SKIP

        Parameters
        ----------
        x : string
            the column to use as the x-axis variable.
        y : string
            the column to use as the y-axis variable.
        c : string, optional
            the column to use to encode the color of the points
        s : string, optional
            the column to use to encode the size of the points
        alpha : float, optional
            transparency level, 0 <= alpha <= 1
        interactive : bool, optional
            if True (default) then produce an interactive plot
        width : int, optional
            the width of the plot in pixels
        height : int, optional
            the height of the plot in pixels

        Returns
        -------
        axes : pdvega.Axes
            The vega-lite plot
        """
        warn_if_keywords_unused('scatter', kwds)
        data = self._data
        cols = [x, y]

        encoding = {
          "x": {
              "field": x,
              "type": infer_vegalite_type(data[x], ordinal_threshold=0)
          },
          "y": {
              "field": y,
              "type": infer_vegalite_type(data[y], ordinal_threshold=0)
          },
        }

        if c is not None:
            cols.append(c)
            encoding['color'] = {
                'field': c,
                'type': infer_vegalite_type(data[c])
            }

        if s is not None:
            cols.append(s)
            encoding['size'] = {
                'field': s,
                'type': infer_vegalite_type(data[s])
            }

        if alpha is not None:
            assert 0 <= alpha <= 1
            encoding['opacity'] = {'value': alpha}

        spec = {
          "mark": "circle",
          "encoding": encoding
        }

        spec = finalize_vegalite_spec(spec, interactive=interactive,
                                      width=width, height=height)
        return Axes(spec, data=data[cols])

    def area(self, x=None, y=None, stacked=True, alpha=None,
             var_name='variable', value_name='value',
             interactive=True, width=450, height=300, **kwds):
        """Area plot for DataFrame data

        >>> dataframe.vgplot.area()  # doctest: +SKIP

        Parameters
        ----------
        x : string, optional
            the column to use as the x-axis variable. If not specified, the
            index will be used.
        y : string, optional
            the column to use as the y-axis variable. If not specified, all
            columns (except x if specified) will be used.
        stacked : bool, optional
            if True (default) then create a stacked area chart. Otherwise,
            areas will overlap
        alpha : float, optional
            transparency level, 0 <= alpha <= 1
        var_name : string, optional
            the legend title
        value_name : string, optional
            the y-axis label
        interactive : bool, optional
            if True (default) then produce an interactive plot
        width : int, optional
            the width of the plot in pixels
        height : int, optional
            the height of the plot in pixels

        Returns
        -------
        axes : pdvega.Axes
            The vega-lite plot
        """
        warn_if_keywords_unused('area', kwds)
        df = unpivot_frame(self._data, x=x, y=y,
                           var_name=var_name, value_name=value_name)
        x = df.columns[0]

        spec = {
          "mark": "area",
          "encoding": {
            "x": {
              "field": x,
              "type": infer_vegalite_type(df[x], ordinal_threshold=0)
            },
            "y": {
              "field": value_name,
              "type": infer_vegalite_type(df[value_name], ordinal_threshold=0),
              "stack": 'zero' if stacked else None
            },
            "color": {
              "field": var_name,
              "type": infer_vegalite_type(df[var_name], ordinal_threshold=10)
            }
          }
        }

        if alpha is None and not stacked and df[var_name].nunique() > 1:
            alpha = 0.7

        if alpha is not None:
            assert 0 <= alpha <= 1
            spec['encoding']['opacity'] = {'value': alpha}

        spec = finalize_vegalite_spec(spec, interactive=interactive,
                                      width=width, height=height)
        return Axes(spec, data=df)

    def bar(self, x=None, y=None, stacked=False, alpha=None,
            var_name='variable', value_name='value',
            interactive=True, width=450, height=300, **kwds):
        """Bar plot for DataFrame data

        >>> dataframe.vgplot.bar()  # doctest: +SKIP

        Parameters
        ----------
        x : string, optional
            the column to use as the x-axis variable. If not specified, the
            index will be used.
        y : string, optional
            the column to use as the y-axis variable. If not specified, all
            columns (except x if specified) will be used.
        stacked : bool, optional
            if True (default) then create a stacked area chart. Otherwise,
            areas will overlap
        alpha : float, optional
            transparency level, 0 <= alpha <= 1
        var_name : string, optional
            the legend title
        value_name : string, optional
            the y-axis label
        interactive : bool, optional
            if True (default) then produce an interactive plot
        width : int, optional
            the width of the plot in pixels
        height : int, optional
            the height of the plot in pixels

        Returns
        -------
        axes : pdvega.Axes
            The vega-lite plot
        """
        warn_if_keywords_unused('bar', kwds)
        df = unpivot_frame(self._data, x=x, y=y,
                           var_name=var_name, value_name=value_name)
        x = df.columns[0]

        spec = {
          "mark": "bar",
          "encoding": {
            "x": {
                "field": x,
                "type": infer_vegalite_type(df[x], ordinal_threshold=50)
            },
            "y": {
                "field": "value",
                "type": infer_vegalite_type(df["value"], ordinal_threshold=0),
                "stack": 'zero' if stacked else None
            },
            "color": {
                "field": "variable",
                "type": infer_vegalite_type(df["variable"])
            },
          },
        }

        if alpha is None and not stacked and df[var_name].nunique() > 1:
            alpha = 0.7

        if alpha is not None:
            assert 0 <= alpha <= 1
            spec['encoding']['opacity'] = {'value': alpha}

        spec = finalize_vegalite_spec(spec, interactive=interactive,
                                      width=width, height=height)
        return Axes(spec, data=df)

    def barh(self, x=None, y=None, stacked=False, alpha=None,
             var_name='variable', value_name='value',
             interactive=True, width=450, height=300, **kwds):
        """Horizontal bar plot for DataFrame data

        >>> dataframe.vgplot.barh()  # doctest: +SKIP

        Parameters
        ----------
        x : string, optional
            the column to use as the x-axis variable. If not specified, the
            index will be used.
        y : string, optional
            the column to use as the y-axis variable. If not specified, all
            columns (except x if specified) will be used.
        stacked : bool, optional
            if True (default) then create a stacked area chart. Otherwise,
            areas will overlap
        alpha : float, optional
            transparency level, 0 <= alpha <= 1
        var_name : string, optional
            the legend title
        value_name : string, optional
            the y-axis label
        interactive : bool, optional
            if True (default) then produce an interactive plot
        width : int, optional
            the width of the plot in pixels
        height : int, optional
            the height of the plot in pixels

        Returns
        -------
        axes : pdvega.Axes
            The vega-lite plot
        """
        plot = self.bar(x=x, y=y, stacked=stacked, alpha=alpha,
                        var_name=var_name, value_name=value_name,
                        interactive=interactive, width=width, height=height,
                        **kwds)
        enc = plot.spec['encoding']
        enc['x'], enc['y'] = enc['y'], enc['x']
        return plot

    def hist(self, x=None, y=None, by=None, bins=10, stacked=False, alpha=None,
             histtype='bar', var_name='variable', value_name='value',
             interactive=True, width=450, height=300, **kwds):
        """Histogram plot for DataFrame data

        >>> dataframe.vgplot.hist()  # doctest: +SKIP

        Parameters
        ----------
        x : string, optional
            the column to use as the x-axis variable. If not specified, the
            index will be used.
        y : string, optional
            the column to use as the y-axis variable. If not specified, all
            columns (except x if specified) will be used.
        by : string, optional
            the column by which to group the results
        bins : integer, optional
            the maximum number of bins to use for the histogram (default: 10)
        stacked : bool, optional
            if True (default) then create a stacked area chart. Otherwise,
            areas will overlap
        alpha : float, optional
            transparency level, 0 <= alpha <= 1
        histtype : string, {'bar', 'step', 'stepfilled'}
            The type of histogram to generate. Default is 'bar'.
        var_name : string, optional
            the legend title
        value_name : string, optional
            the y-axis label
        interactive : bool, optional
            if True (default) then produce an interactive plot
        width : int, optional
            the width of the plot in pixels
        height : int, optional
            the height of the plot in pixels

        Returns
        -------
        axes : pdvega.Axes
            The vega-lite plot
        """
        warn_if_keywords_unused('hist', kwds)
        if by is not None:
            raise NotImplementedError('vgplot.hist `by` keyword')
        if x is not None or y is not None:
            raise NotImplementedError('"x" and "y" args to hist()')
        df = self._data.melt(var_name=var_name, value_name=value_name)

        if histtype in ['bar', 'barstacked']:
            mark = 'bar'
        elif histtype == 'stepfilled':
            mark = {'type': 'area', 'interpolate': 'step'}
        elif histtype == 'step':
            mark = {'type': 'line', 'interpolate': 'step'}
        else:
            raise ValueError("histtype '{0}' is not recognized"
                             "".format(histtype))

        spec = {
            "mark": mark,
            "encoding": {
                "x": {
                    "bin": {"maxbins": bins},
                    "field": value_name,
                    "type": "quantitative"
                },
                "y": {
                    "aggregate": "count",
                    "type": "quantitative",
                    "stack": ('zero' if stacked else None)
                },
                "color": {
                    "field": var_name,
                    "type": "nominal"
                },
            },
        }

        if alpha is None and not stacked and df[var_name].nunique() > 1:
            alpha = 0.7

        if alpha is not None:
            assert 0 <= alpha <= 1
            spec['encoding']['opacity'] = {'value': alpha}

        spec = finalize_vegalite_spec(spec, interactive=interactive,
                                      width=width, height=height)
        return Axes(spec, data=df)

    def heatmap(self, x, y, C=None, reduce_C_function=None,
                gridsize=100, alpha=None,
                interactive=True, width=450, height=300, **kwds):
        """Heatmap plot for DataFrame data

        Note that Vega-Lite does not support hexagonal binning, so this method
        returns a cartesian heatmap.

        >>> dataframe.vgplot.hexbin()  # doctest: +SKIP

        Parameters
        ----------
        x : string
            the column to use as the x-axis variable.
        y : string
            the column to use as the y-axis variable.
        C : string, optional
            the column to use to compute the mean within each bin. If not
            specified, the count within each bin will be used.
        reduce_C_function : callable, optional
            the type of reduction to be done within each bin (not implemented)
        gridsize : int, optional
            the number of divisions in the x and y axis (default=100)
        alpha : float, optional
            transparency level, 0 <= alpha <= 1
        interactive : bool, optional
            if True (default) then produce an interactive plot
        width : int, optional
            the width of the plot in pixels
        height : int, optional
            the height of the plot in pixels

        Returns
        -------
        axes : pdvega.Axes
            The vega-lite plot
        """
        # TODO: Use actual hexbins rather than a grid heatmap
        warn_if_keywords_unused('hexbin', kwds)

        if reduce_C_function is not None:
            raise NotImplementedError("Custom reduce_C_function in hexbin")
        if C is None:
            df = self._data[[x, y]]
        else:
            df = self._data[[x, y, C]]

        spec = {
          "mark": "rect",
          "encoding": {
            "x": {"field": x, "bin": {"maxbins": gridsize}, "type": "quantitative"},
            "y": {"field": y, "bin": {"maxbins": gridsize}, "type": "quantitative"},
            "color": ({"aggregate": "count", "type": "quantitative"} if C is None else
                      {"field": C, "aggregate": "mean", "type": "quantitative"})
          },
          "config": {
            "range": {
              "heatmap": {
                "scheme": "greenblue"
              }
            },
            "view": {
              "stroke": "transparent"
            }
          },
          "mark": "rect",
        }

        if alpha is not None:
            assert 0 <= alpha <= 1
            spec['encoding']['opacity'] = {'value': alpha}

        spec = finalize_vegalite_spec(spec, interactive=interactive,
                                      width=width, height=height)
        return Axes(spec, data=df)

    hexbin = heatmap

    def kde(self, x=None, y=None, bw_method=None, alpha=None,
            interactive=True, width=450, height=300, **kwds):
        """Kernel Density Estimate plot for DataFrame data

        >>> dataframe.vgplot.kde()  # doctest: +SKIP

        Parameters
        ----------
        x : string, optional
            the column to use as the x-axis variable. If not specified, the
            index will be used.
        y : string, optional
            the column to use as the y-axis variable. If not specified, all
            columns (except x if specified) will be used.
        bw_method : str, scalar or callable, optional
            The method used to calculate the estimator bandwidth. This can be
            'scott', 'silverman', a scalar constant or a callable.
            See `scipy.stats.gaussian_kde` for more details.
        alpha : float, optional
            transparency level, 0 <= alpha <= 1
        interactive : bool, optional
            if True (default) then produce an interactive plot
        width : int, optional
            the width of the plot in pixels
        height : int, optional
            the height of the plot in pixels

        Returns
        -------
        axes : pdvega.Axes
            The vega-lite plot
        """
        from scipy.stats import gaussian_kde as kde
        if x is not None:
            raise NotImplementedError('"x" argument to df.vgplot.kde()')

        if y is not None:
            df = self._data[y].to_frame()
        else:
            df = self._data

        tmin, tmax = df.min().min(), df.max().max()
        trange = tmax - tmin
        t = np.linspace(tmin - 0.5 * trange, tmax + 0.5 * trange, 1000)

        kde_df = pd.DataFrame({col: kde(df[col], bw_method=bw_method).evaluate(t)
                               for col in df}, index=t)
        kde_df.index.name = ' '

        f = FramePlotMethods(kde_df)
        return f.line(value_name='Density', alpha=alpha,
                      interactive=interactive,
                      width=width, height=height, **kwds)

    density = kde
