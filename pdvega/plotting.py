"""Core plotting routines"""
import warnings
import altair as alt
import numpy as np
import pandas as pd

from ._utils import infer_vegalite_type

__all__ = ["scatter_matrix", "andrews_curves", "parallel_coordinates", "lag_plot"]


def scatter_matrix(frame, c=None, s=None, figsize=None, dpi=72.0, **kwds):
    """Draw a matrix of scatter plots.

    The result is an interactive pan/zoomable plot, with linked-brushing
    enabled by holding the shift key.

    Parameters
    ----------
    frame : DataFrame
        The dataframe for which to draw the scatter matrix.
    c : string (optional)
        If specified, the name of the column to be used to determine the
        color of each point.
    s : string (optional)
        If specified, the name of the column to be used to determine the
        size of each point,
    figsize : tuple (optional)
        A length-2 tuple speficying the size of the figure in inches
    dpi : float (default=72)
        The dots (i.e. pixels) per inch used to convert the figure size from
        inches to pixels.

    Returns
    -------
    chart: alt.Chart object
        The alt.Chart representation of the plot.

    See Also
    --------
    pandas.plotting.scatter_matrix : matplotlib version of this routine
    """
    if kwds:
        warnings.warn(
            "Unrecognized keywords in pdvega.scatter_matrix: {0}"
            "".format(list(kwds.keys()))
        )

    cols = [
        col
        for col in frame.columns
        if col not in [c, s]
        if infer_vegalite_type(frame[col], ordinal_threshold=0) == "quantitative"
    ]

    spec = {
        "$schema": "https://vega.github.io/schema/vega-lite/v2.json",
        "repeat": {"row": cols, "column": cols[::-1]},
        "spec": {
            "mark": "point",
            "selection": {
                "brush": {
                    "type": "interval",
                    "resolve": "union",
                    "on": "[mousedown[event.shiftKey], window:mouseup] > window:mousemove!",
                    "translate": "[mousedown[event.shiftKey], window:mouseup] > window:mousemove!",
                    "zoom": "wheel![event.shiftKey]",
                },
                "grid": {
                    "type": "interval",
                    "resolve": "global",
                    "bind": "scales",
                    "translate": "[mousedown[!event.shiftKey], window:mouseup] > window:mousemove!",
                    "zoom": "wheel![!event.shiftKey]",
                },
            },
            "encoding": {
                "x": {"field": {"repeat": "column"}, "type": "quantitative"},
                "y": {"field": {"repeat": "row"}, "type": "quantitative"},
                "color": {"condition": {"selection": "brush"}, "value": "grey"},
            },
        },
    }

    if figsize is not None:
        width_inches, height_inches = figsize
        spec["spec"]["width"] = 0.8 * dpi * width_inches / len(cols)
        spec["spec"]["height"] = 0.8 * dpi * height_inches / len(cols)

    if s is not None:
        spec["spec"]["encoding"]["size"] = {
            "field": s, "type": infer_vegalite_type(frame[s])
        }

    cond = spec["spec"]["encoding"]["color"]["condition"]
    if c is None:
        cond["value"] = "steelblue"
    else:
        cond["field"] = c
        cond["type"] = infer_vegalite_type(frame[c])

    chart = alt.Chart().from_dict(spec)
    chart.data = frame
    return chart


def andrews_curves(
    data, class_column, samples=200, alpha=None, width=450, height=300, **kwds
):
    """
    Generates an Andrews curves visualization for visualising clusters of
    multivariate data.

    Andrews curves have the functional form:

    f(t) = x_1/sqrt(2) + x_2 sin(t) + x_3 cos(t) +
           x_4 sin(2t) + x_5 cos(2t) + ...

    Where x coefficients correspond to the values of each dimension and t is
    linearly spaced between -pi and +pi. Each row of frame then corresponds to
    a single curve.

    Parameters:
    -----------
    data : DataFrame
        Data to be plotted, preferably normalized to (0.0, 1.0)
    class_column : string
        Name of the column containing class names
    samples : integer
        Number of points to plot in each curve
    alpha: float, optional
        The transparency of the lines
    width : int, optional
        the width of the plot in pixels
    height : int, optional
        the height of the plot in pixels
    **kwds: keywords
        Additional options

    Returns:
    --------
    chart: alt.Chart object

    """
    if kwds:
        warnings.warn(
            "Unrecognized keywords in pdvega.andrews_curves(): {0}"
            "".format(list(kwds.keys()))
        )

    t = np.linspace(-np.pi, np.pi, samples)
    vals = data.drop(class_column, axis=1).values.T

    curves = np.outer(vals[0], np.ones_like(t))
    for i in range(1, len(vals)):
        ft = ((i + 1) // 2) * t
        if i % 2 == 1:
            curves += np.outer(vals[i], np.sin(ft))
        else:
            curves += np.outer(vals[i], np.cos(ft))

    df = pd.DataFrame(
        {
            "t": np.tile(t, curves.shape[0]),
            "sample": np.repeat(np.arange(curves.shape[0]), curves.shape[1]),
            " ": curves.ravel(),
            class_column: np.repeat(data[class_column], samples),
        }
    )

    chart = alt.Chart(df).properties(width=width, height=height).mark_line()
    chart = chart.encode(
        x=alt.X(field="t", type="quantitative"),
        y=alt.Y(field=" ", type="quantitative"),
        color=alt.Color(field=class_column, type=infer_vegalite_type(df[class_column])),
        detail=alt.Detail(field='sample', type="quantitative")
    )

    if alpha is None and df[class_column].nunique() > 20:
        alpha = 0.5

    if alpha is not None:
        assert 0 <= alpha <= 1
        return chart.encode(opacity=alt.value(alpha))

    return chart


def parallel_coordinates(
    data,
    class_column,
    cols=None,
    alpha=None,
    width=450,
    height=300,
    interactive=True,
    var_name="variable",
    value_name="value",
    **kwds
):
    """
    Parallel coordinates plotting.

    Parameters
    ----------
    frame: DataFrame
    class_column: str
        Column name containing class names
    cols: list, optional
        A list of column names to use
    alpha: float, optional
        The transparency of the lines
    interactive : bool, optional
        if True (default) then produce an interactive plot
    width : int, optional
        the width of the plot in pixels
    height : int, optional
        the height of the plot in pixels
    var_name : string, optional
        the legend title
    value_name : string, optional
        the y-axis label

    Returns
    -------
    chart: alt.Chart object
        The altair representation of the plot.

    See Also
    --------
    pandas.plotting.parallel_coordinates : matplotlib version of this routine
    """
    if kwds:
        warnings.warn(
            "Unrecognized keywords in pdvega.scatter_matrix: {0}"
            "".format(list(kwds.keys()))
        )

    # Transform the dataframe to be used in Vega-Lite
    if cols is not None:
        data = data[list(cols) + [class_column]]
    cols = data.columns
    df = data.reset_index()
    index = (set(df.columns) - set(cols)).pop()
    assert index in df.columns
    df = df.melt([index, class_column], var_name=var_name, value_name=value_name)

    chart = alt.Chart(df).properties(width=width, height=height)
    chart = chart.mark_line().encode(
         x=alt.X(field=var_name, type=infer_vegalite_type(df[var_name])),
         y=alt.Y(field=value_name, type=infer_vegalite_type(df[value_name])),
         color=alt.Color(field=class_column, type=infer_vegalite_type(df[class_column])),
         detail=alt.Detail(field=index, type=infer_vegalite_type(df[index]))
    )

    if alpha is None and df[class_column].nunique() > 20:
        alpha = 0.3

    if alpha is not None:
        assert 0 <= alpha <= 1
        return chart.encode(opacity=alt.value(alpha))
    return chart


def lag_plot(data, lag=1, kind="scatter", **kwds):
    """Lag plot for time series.

    Parameters
    ----------
    data: pandas.Series
        the time series to plot
    lag: integer
        The lag of the scatter plot, default=1
    kind: string
        The kind of plot to use (e.g. 'scatter', 'line')
    **kwds:
        Additional keywords passed to data.vgplot.scatter

    Returns
    -------
    chart: alt.Chart object
    """
    if lag != int(lag) or int(lag) <= 0:
        raise ValueError("lag must be a positive integer")
    lag = int(lag)

    values = data.values
    y1 = "y(t)"
    y2 = "y(t + {0})".format(lag)
    lags = pd.DataFrame({y1: values[:-lag].T.ravel(), y2: values[lag:].T.ravel()})

    if isinstance(data, pd.DataFrame):
        lags["variable"] = np.repeat(data.columns, lags.shape[0] / data.shape[1])
        kwds["c"] = "variable"

    return lags.vgplot(kind=kind, x=y1, y=y2, **kwds)
