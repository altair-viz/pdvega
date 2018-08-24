import numpy as np
import pandas as pd
import altair as alt

from ._utils import (
    infer_vegalite_type,
    unpivot_frame,
    warn_if_keywords_unused,
    validate_aggregation,
)
from ._pandas_internals import (
    PandasObject,
    register_dataframe_accessor,
    register_series_accessor,
)


def _x(x, df, ordinal_threshold=6, **kwargs):
    return alt.X(
        field=x,
        type=infer_vegalite_type(df[x], ordinal_threshold=ordinal_threshold),
        **kwargs
    )


def _y(y, df, ordinal_threshold=6, **kwargs):
    return alt.Y(
        field=y,
        type=infer_vegalite_type(df[y], ordinal_threshold=ordinal_threshold),
        **kwargs
    )


class BasePlotMethods(PandasObject):

    def __init__(self, data):
        self._data = data

    def __call__(self, kind, *args, **kwargs):
        raise NotImplementedError()

    def _plot(self, data=None, width=450, height=300, title=None):

        if data is None:
            data = self._data

        if title is None:
            title = ""

        chart = alt.Chart(data=data).properties(width=width, height=height, title=title)
        return chart


@register_series_accessor("vgplot")
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

    def __call__(self, kind="line", **kwargs):
        try:
            plot_method = getattr(self, kind)
        except AttributeError:
            raise ValueError(
                "kind='{0}' not valid for {1}" "".format(kind, self.__class__.__name__)
            )
        return plot_method(**kwargs)

    def line(self, alpha=None, width=450, height=300, ax=None, **kwds):
        """Line plot for Series data

        >>> series.vgplot.line()  # doctest: +SKIP

        Parameters
        ----------
        alpha : float, optional
            transparency level, 0 <= alpha <= 1
        width : int, optional
            the width of the plot in pixels
        height : int, optional
            the height of the plot in pixels
        ax: altair.Chart, optional
            chart to be overlayed with this vis (convinience method for `chart1 + chart2`)

        Returns
        -------
        chart : altair.Chart
            The altair plot representation
        """
        warn_if_keywords_unused("line", kwds)
        df = self._data.reset_index()
        df.columns = map(str, df.columns)
        x, y = df.columns

        chart = self._plot(
            data=df, width=width, height=height, title=kwds.get("title", "")
        )

        chart = chart.mark_line().encode(x=_x(x, df), y=_y(y, df))

        if alpha is not None:
            assert 0 <= alpha <= 1
            chart = chart.encode(opacity=alt.value(alpha))

        if ax is not None:
            return ax + chart
        return chart

    def area(self, alpha=None, width=450, height=300, ax=None, **kwds):
        """Area plot for Series data

        >>> series.vgplot.area()  # doctest: +SKIP

        Parameters
        ----------
        alpha : float, optional
            transparency level, 0 <= alpha <= 1
        width : int, optional
            the width of the plot in pixels
        height : int, optional
            the height of the plot in pixels
        ax: altair.Chart, optional
            chart to be overlayed with this vis (convinience method for `chart1 + chart2`)

        Returns
        -------
        chart : alt.Chart
            altair chart representation
        """
        warn_if_keywords_unused("area", kwds)
        df = self._data.reset_index()
        df.columns = map(str, df.columns)
        x, y = df.columns

        chart = self._plot(
            data=df, width=width, height=height, title=kwds.get("title", "")
        )

        chart = chart.mark_area().encode(x=_x(x, df), y=_y(y, df))

        if alpha is not None:
            assert 0 <= alpha <= 1
            chart = chart.encode(opacity=alt.value(alpha))

        if ax is not None:
            return ax + chart
        return chart

    def bar(self, alpha=None, width=450, height=300, ax=None, **kwds):
        """Bar plot for Series data

        >>> series.vgplot.bar()  # doctest: +SKIP

        Parameters
        ----------
        alpha : float, optional
            transparency level, 0 <= alpha <= 1
        width : int, optional
            the width of the plot in pixels
        height : int, optional
            the height of the plot in pixels
        ax: altair.Chart, optional
            chart to be overlayed with this vis (convinience method for `chart1 + chart2`)

        Returns
        -------
        chart : alt.Chart
            altair chart representation
        """
        warn_if_keywords_unused("bar", kwds)

        df = self._data.reset_index()
        df.columns = map(str, df.columns)
        x, y = df.columns

        chart = self._plot(
            data=df, width=width, height=height, title=kwds.get("title", "")
        )

        chart = chart.mark_bar().encode(x=_x(x, df), y=_y(y, df))

        if alpha is not None:
            assert 0 <= alpha <= 1
            chart = chart.encode(opacity=alt.value(alpha))

        if ax is not None:
            return ax + chart
        return chart

    def barh(self, alpha=None, width=450, height=300, ax=None, **kwds):
        """Horizontal bar plot for Series data

        >>> series.vgplot.barh()  # doctest: +SKIP

        Parameters
        ----------
        alpha : float, optional
            transparency level, 0 <= alpha <= 1
        width : int, optional
            the width of the plot in pixels
        height : int, optional
            the height of the plot in pixels
        ax: altair.Chart, optional
            chart to be overlayed with this vis (convinience method for `chart1 + chart2`)

        Returns
        -------
        chart : alt.Chart
            altair chart representation
        """
        chart = self.bar(alpha=alpha, width=width, height=height, **kwds)

        enc = chart.encoding
        enc["x"], enc["y"] = enc["y"], enc["x"]

        if ax is not None:
            return ax + chart
        return chart

    def hist(self, bins=10, alpha=None, histtype="bar", width=450, height=300, ax=None, **kwds):
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
        width : int, optional
            the width of the plot in pixels
        height : int, optional
            the height of the plot in pixels
        ax: altair.Chart, optional
            chart to be overlayed with this vis (convinience method for `chart1 + chart2`)

        Returns
        -------
        chart : alt.Chart
            altair chart representation
        """
        warn_if_keywords_unused("hist", kwds)
        df = self._data.to_frame().reset_index(drop=False)
        df.columns = df.columns.astype(str)
        y, x = df.columns

        marks = {
            "bar": "bar",
            "barstacked": "bar",
            "stepfilled": {"type": "area", "interpolate": "step"},
            "step": {"type": "line", "interpolate": "step"},
        }

        if histtype in marks:
            mark = marks[histtype]
        else:
            raise ValueError("histtype '{0}' is not recognized" "".format(histtype))

        chart = self._plot(
            data=df, width=width, height=height, title=kwds.get("title", "")
        )

        chart.mark = mark
        chart = chart.encode(
            x=_x(x, df, bin={"maxbins": 5}), y=_y(y, df, aggregate="count")
        )

        if alpha is not None:
            assert 0 <= alpha <= 1
            chart = chart.encode(opacity=alt.value(alpha))

        if ax is not None:
            return ax + chart
        return chart

    def kde(self, bw_method=None, alpha=None, width=450, height=300, ax=None, **kwds):
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
        width : int, optional
            the width of the plot in pixels
        height : int, optional
            the height of the plot in pixels
        ax: altair.Chart, optional
            chart to be overlayed with this vis (convinience method for `chart1 + chart2`)

        Returns
        -------
        chart : alt.Chart
            altair chart representation
        """
        from scipy.stats import gaussian_kde

        data = self._data
        tmin, tmax = data.min(), data.max()
        trange = tmax - tmin
        t = np.linspace(tmin - 0.5 * trange, tmax + 0.5 * trange, 1000)

        kde_ser = pd.Series(
            gaussian_kde(data, bw_method=bw_method).evaluate(t), index=t, name=data.name
        )

        kde_ser.index.name = " "
        f = self.__class__(kde_ser)
        return f.line(alpha=alpha, width=width, height=height, ax=ax, **kwds)

    density = kde


@register_dataframe_accessor("vgplot")
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

    def __call__(self, x=None, y=None, kind="line", **kwargs):
        try:
            plot_method = getattr(self, kind)
        except AttributeError:
            raise ValueError(
                "kind='{0}' not valid for {1}" "".format(kind, self.__class__.__name__)
            )
        return plot_method(x=x, y=y, **kwargs)

    def line(
        self,
        x=None,
        y=None,
        alpha=None,
        var_name="variable",
        value_name="value",
        width=450,
        height=300,
        ax=None,
        **kwds
    ):
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
        width : int, optional
            the width of the plot in pixels
        height : int, optional
            the height of the plot in pixels
        ax: altair.Chart, optional
            chart to be overlayed with this vis (convinience method for `chart1 + chart2`)

        Returns
        -------
        chart : alt.Chart
            altair chart representation
        """
        warn_if_keywords_unused("line", kwds)
        use_order = (x is not None)

        if use_order:
            df = self._data.reset_index()
            order = df.columns[0]
            df = unpivot_frame(
                df, x=(x, order), y=y, var_name=var_name, value_name=value_name
            )
        else:
            df = unpivot_frame(
                self._data, x=x, y=y, var_name=var_name, value_name=value_name
            )
            x = df.columns[0]

        chart = self._plot(
            data=df, width=width, height=height, title=kwds.get("title", None)
        )

        chart = chart.mark_line().encode(
            x=_x(x, df), y=_y(value_name, df), color=alt.Color(var_name, type="nominal")
        )

        if alpha is not None:
            assert 0 <= alpha <= 1
            chart = chart.encode(opacity=alt.value(alpha))

        if use_order:
            chart.encoding["order"] = {
                "field": order, "type": infer_vegalite_type(df[order])
            }

        if ax is not None:
            return ax + chart
        return chart

    def scatter(
        self,
        x,
        y,
        c=None,
        s=None,
        alpha=None,
        width=450,
        height=300,
        ax=None,
        **kwds
    ):
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
        width : int, optional
            the width of the plot in pixels
        height : int, optional
            the height of the plot in pixels
        ax: altair.Chart, optional
            chart to be overlayed with this vis (convinience method for `chart1 + chart2`)

        Returns
        -------
        chart : alt.Chart
            altair chart representation
        """
        warn_if_keywords_unused("scatter", kwds)
        df = self._data

        chart = self._plot(width=width, height=height, title=kwds.get("title", ""))
        chart = chart.mark_point().encode(x=_x(x, df, ordinal_threshold=0), y=_y(y, df, ordinal_threshold=0))

        if alpha is not None:
            assert 0 <= alpha <= 1
            chart = chart.encode(opacity=alt.value(alpha))

        if c is not None:
            chart.encoding["color"] = {"field": c, "type": infer_vegalite_type(df[c])}

        if s is not None:
            chart.encoding["size"] = {"field": s, "type": infer_vegalite_type(df[s])}

        if ax is not None:
            return ax + chart
        return chart

    def area(
        self,
        x=None,
        y=None,
        stacked=True,
        alpha=None,
        var_name="variable",
        value_name="value",
        width=450,
        height=300,
        ax=None,
        **kwds
    ):
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
        width : int, optional
            the width of the plot in pixels
        height : int, optional
            the height of the plot in pixels
        ax: altair.Chart, optional
            chart to be overlayed with this vis (convinience method for `chart1 + chart2`)

        Returns
        -------
        chart : alt.Chart
            altair chart representation
        """
        warn_if_keywords_unused("area", kwds)
        df = unpivot_frame(
            self._data, x=x, y=y, var_name=var_name, value_name=value_name
        )

        x = df.columns[0]

        if alpha is None and not stacked and df[var_name].nunique() > 1:
            alpha = 0.7

        chart = self._plot(
            data=df, width=width, height=height, title=kwds.get("title", None)
        )
        chart = chart.mark_area().encode(
            x=_x(x, df),
            y=alt.Y(
                value_name,
                type=infer_vegalite_type(df[value_name]),
                stack=(None, "zero")[stacked],
            ),
            color=alt.Color(field=var_name, type=infer_vegalite_type(df[var_name])),
        )

        if alpha is not None:
            assert 0 <= alpha <= 1
            chart = chart.encode(opacity=alt.value(alpha))

        if ax is not None:
            return ax + chart
        return chart

    def bar(
        self,
        x=None,
        y=None,
        stacked=False,
        alpha=None,
        var_name="variable",
        value_name="value",
        width=450,
        height=300,
        ax=None,
        **kwds
    ):
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
        width : int, optional
            the width of the plot in pixels
        height : int, optional
            the height of the plot in pixels
        ax: altair.Chart, optional
            chart to be overlayed with this vis (convinience method for `chart1 + chart2`)

        Returns
        -------
        chart : alt.Chart
            altair chart representation
        """
        warn_if_keywords_unused("bar", kwds)
        df = unpivot_frame(
            self._data, x=x, y=y, var_name=var_name, value_name=value_name
        )
        x = df.columns[0]

        if alpha is None and not stacked and df[var_name].nunique() > 1:
            alpha = 0.7

        chart = self._plot(
            data=df, width=width, height=height, title=kwds.get("title", None)
        )
        chart = chart.mark_bar().encode(
            x=alt.X(x, type=infer_vegalite_type(df[x], ordinal_threshold=50)),
            y=alt.Y(
                "value",
                type=infer_vegalite_type(df["value"]),
                stack=(None, "zero")[stacked],
            ),
            color=alt.Color(field="variable", type=infer_vegalite_type(df["variable"])),
        )

        if alpha is not None:
            assert 0 <= alpha <= 1
            chart = chart.encode(opacity=alt.value(alpha))

        if ax is not None:
            return ax + chart
        return chart

    def barh(
        self,
        x=None,
        y=None,
        stacked=False,
        alpha=None,
        var_name="variable",
        value_name="value",
        width=450,
        height=300,
        ax=None,
        **kwds
    ):
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
        width : int, optional
            the width of the plot in pixels
        height : int, optional
            the height of the plot in pixels
        ax: altair.Chart, optional
            chart to be overlayed with this vis (convinience method for `chart1 + chart2`)

        Returns
        -------
        chart : alt.Chart
            altair chart representation
        """
        chart = self.bar(
            x=x,
            y=y,
            stacked=stacked,
            alpha=alpha,
            var_name=var_name,
            value_name=value_name,
            width=width,
            height=height,
            **kwds
        )

        enc = chart.encoding
        enc["x"], enc["y"] = enc["y"], enc["x"]
        if ax is not None:
            return ax + chart
        return chart

    def hist(
        self,
        x=None,
        y=None,
        by=None,
        bins=10,
        stacked=False,
        alpha=None,
        histtype="bar",
        var_name="variable",
        value_name="value",
        width=450,
        height=300,
        ax=None,
        **kwds
    ):
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
        width : int, optional
            the width of the plot in pixels
        height : int, optional
            the height of the plot in pixels
        ax: altair.Chart, optional
            chart to be overlayed with this vis (convinience method for `chart1 + chart2`)

        Returns
        -------
        chart : alt.Chart
            altair chart representation
        """
        warn_if_keywords_unused("hist", kwds)
        if by is not None:
            raise NotImplementedError("vgplot.hist `by` keyword")
        if x is not None or y is not None:
            raise NotImplementedError('"x" and "y" args to hist()')
        df = self._data.melt(var_name=var_name, value_name=value_name)

        marks = {
            "bar": "bar",
            "barstacked": "bar",
            "stepfilled": {"type": "area", "interpolate": "step"},
            "step": {"type": "line", "interpolate": "step"},
        }

        if histtype in marks:
            mark = marks[histtype]
        else:
            raise ValueError("histtype '{0}' is not recognized" "".format(histtype))

        if alpha is None and not stacked and df[var_name].nunique() > 1:
            alpha = 0.7

        chart = self._plot(
            data=df, width=width, height=height, title=kwds.get("title", None)
        )
        chart.mark = mark
        chart = chart.encode(
            x=alt.X(value_name, bin={"maxbins": bins}, type="quantitative"),
            y=alt.Y(
                aggregate="count",
                type="quantitative",
                stack=("zero" if stacked else None),
            ),
            color=alt.Color(field=var_name, type="nominal"),
        )

        if alpha is not None:
            assert 0 <= alpha <= 1
            chart = chart.encode(opacity=alt.value(alpha))

        if ax is not None:
            return ax + chart
        return chart

    def heatmap(
        self,
        x,
        y,
        C=None,
        reduce_C_function="mean",
        gridsize=100,
        alpha=None,
        width=450,
        height=300,
        ax=None,
        **kwds
    ):
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
        reduce_C_function : string, default = 'mean'
            One of ['mean', 'sum', 'median', 'min', 'max', 'count'], or
            associated numpy or python builtin functions. Note that arbitrary
            callable functions are not supported.
        gridsize : int, optional
            the number of divisions in the x and y axis (default=100)
        alpha : float, optional
            transparency level, 0 <= alpha <= 1
        width : int, optional
            the width of the plot in pixels
        height : int, optional
            the height of the plot in pixels
        ax: altair.Chart, optional
            chart to be overlayed with this vis (convinience method for `chart1 + chart2`)

        Returns
        -------
        chart : alt.Chart
            altair chart representation
        """
        # TODO: Use actual hexbins rather than a grid heatmap
        warn_if_keywords_unused("hexbin", kwds)
        reduce_C_function = validate_aggregation(reduce_C_function)

        if C is None:
            df = self._data[[x, y]]
        else:
            df = self._data[[x, y, C]]

        if C is None:
            color = alt.Color(aggregate="count", type="quantitative")
        else:
            color = alt.Color(field=C, aggregate=reduce_C_function,
                              type="quantitative")
        color.scale = alt.Scale(scheme='greens')

        chart = self._plot(
            data=df, width=width, height=height, title=kwds.get("title", None)
        ).mark_rect().encode(
            x=alt.X(x, bin=alt.Bin(maxbins=gridsize), type="quantitative"),
            y=alt.Y(y, bin=alt.Bin(maxbins=gridsize), type="quantitative"),
            color=color
        )

        if alpha is not None:
            assert 0 <= alpha <= 1
            chart = chart.encode(opacity=alt.value(alpha))

        if ax is not None:
            return ax + chart
        return chart

    hexbin = heatmap

    def kde(
        self,
        x=None,
        y=None,
        bw_method=None,
        alpha=None,
        width=450,
        height=300,
        ax=None,
        **kwds
    ):
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
        width : int, optional
            the width of the plot in pixels
        height : int, optional
            the height of the plot in pixels
        ax: altair.Chart, optional
            chart to be overlayed with this vis (convinience method for `chart1 + chart2`)

        Returns
        -------
        chart : alt.Chart
            altair chart representation
        """
        from scipy.stats import gaussian_kde as kde

        if x is not None:  # ??
            raise NotImplementedError('"x" argument to df.vgplot.kde()')

        if y is not None:
            df = self._data[y].to_frame()
        else:
            df = self._data

        tmin, tmax = df.min().min(), df.max().max()
        trange = tmax - tmin
        t = np.linspace(tmin - 0.5 * trange, tmax + 0.5 * trange, 1000)

        kde_df = pd.DataFrame(
            {col: kde(df[col], bw_method=bw_method).evaluate(t) for col in df}, index=t
        )
        kde_df.index.name = " "

        f = FramePlotMethods(kde_df)
        return f.line(
            value_name="Density",
            alpha=alpha,
            width=width,
            height=height,
            ax=ax,
            **kwds
        )

    density = kde
