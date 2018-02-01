"""Core plotting routines"""
import warnings

import numpy as np
import pandas as pd

from ._axes import Axes
from ._utils import infer_vegalite_type, finalize_vegalite_spec

__all__ = ['scatter_matrix', 'andrews_curves', 'parallel_coordinates',
           'lag_plot']


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
    plot : VegaLite object
        The Vega-Lite representation of the plot.

    See Also
    --------
    pandas.plotting.scatter_matrix : matplotlib version of this routine
    """
    if kwds:
        warnings.warn("Unrecognized keywords in pdvega.scatter_matrix: {0}"
                      "".format(list(kwds.keys())))
    cols = [col for col in frame.columns
            if col not in [c, s]
            if infer_vegalite_type(frame[col], ordinal_threshold=0) == 'quantitative']
    spec = {
      "$schema": "https://vega.github.io/schema/vega-lite/v2.json",
      "repeat": {
        "row": cols,
        "column": cols[::-1]
      },
      "spec": {
        "mark": "point",
        "selection": {
          "brush": {
            "type": "interval",
            "resolve": "union",
            "on": "[mousedown[event.shiftKey], window:mouseup] > window:mousemove!",
            "translate": "[mousedown[event.shiftKey], window:mouseup] > window:mousemove!",
            "zoom": "wheel![event.shiftKey]"
          },
          "grid": {
            "type": "interval",
            "resolve": "global",
            "bind": "scales",
            "translate": "[mousedown[!event.shiftKey], window:mouseup] > window:mousemove!",
            "zoom": "wheel![!event.shiftKey]"
          }
        },
        "encoding": {
          "x": {"field": {"repeat": "column"}, "type": "quantitative"},
          "y": {"field": {"repeat": "row"}, "type": "quantitative"},
          "color": {
            "condition": {
              "selection": "brush",
            },
            "value": "grey"
          }
        },
      }
    }

    if figsize is not None:
        width_inches, height_inches = figsize
        spec['spec']['width'] = 0.8 * dpi * width_inches / len(cols)
        spec['spec']['height'] = 0.8 * dpi * height_inches / len(cols)

    if s is not None:
        spec['spec']['encoding']["size"] = {
            "field": s,
            "type": infer_vegalite_type(frame[s])
        }

    cond = spec['spec']['encoding']['color']['condition']
    if c is None:
        cond['value'] = 'steelblue'
    else:
        cond['field'] = c
        cond['type'] = infer_vegalite_type(frame[c])
    return Axes(spec, data=frame)


def andrews_curves(data, class_column, samples=200, alpha=None,
                   width=450, height=300, interactive=True, **kwds):
    if kwds:
        warnings.warn("Unrecognized keywords in pdvega.andrews_curves(): {0}"
                      "".format(list(kwds.keys())))
    t = np.linspace(-np.pi, np.pi, samples)
    vals = data.drop(class_column, axis=1).values.T

    curves = np.outer(vals[0], np.ones_like(t))
    for i in range(1, len(vals)):
        ft = ((i + 1) // 2) * t
        if i % 2 == 1:
            curves += np.outer(vals[i], np.sin(ft))
        else:
            curves += np.outer(vals[i], np.cos(ft))

    df = pd.DataFrame({'t': np.tile(np.arange(samples), curves.shape[0]),
                       'sample': np.repeat(np.arange(curves.shape[0]), curves.shape[1]),
                       ' ': curves.ravel(),
                       class_column: np.repeat(data[class_column], samples)})

    spec = {
        'mark': 'line',
        'encoding': {
            'x': {'field': 't', 'type': 'quantitative'},
            'y': {'field': ' ', 'type': 'quantitative'},
            'color': {'field': class_column, 'type': infer_vegalite_type(df[class_column])},
            'detail': {'field': 'sample', 'type': 'quantitative'}
        }
    }
    if alpha is not None:
        assert 0 <= alpha <= 1
        spec['encoding']['opacity'] = {'value': alpha}

    spec = finalize_vegalite_spec(spec, width=width, height=height, interactive=interactive)

    return Axes(spec, data=df)


def parallel_coordinates(data, class_column, cols=None, alpha=None,
                         width=450, height=300, interactive=True,
                         var_name='variable', value_name='value', **kwds):
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

    Returns
    -------
    plot : VegaLite object
        The Vega-Lite representation of the plot.

    See Also
    --------
    pandas.plotting.parallel_coordinates : matplotlib version of this routine
    """
    if kwds:
        warnings.warn("Unrecognized keywords in pdvega.scatter_matrix: {0}"
                      "".format(list(kwds.keys())))

    # Transform the dataframe to be used in Vega-Lite
    if cols is not None:
        data = data[list(cols) + [class_column]]
    cols = data.columns
    df = data.reset_index()
    index = (set(df.columns) - set(cols)).pop()
    assert index in df.columns
    df = df.melt([index, class_column],
                 var_name=var_name, value_name=value_name)

    spec = {
        'mark': 'line',
        'encoding': {
            'color': {
                'field': class_column,
                'type': infer_vegalite_type(df[class_column])
            },
            'detail': {
                'field': index,
                'type': infer_vegalite_type(df[index])
            },
            'x': {
                'field': var_name,
                'type': infer_vegalite_type(df[var_name])
            },
            'y': {
                'field': value_name,
                'type': infer_vegalite_type(df[value_name])
            }
        }
    }

    if alpha is not None:
        assert 0 <= alpha <= 1
        spec['encoding']['opacity'] = {'value': alpha}

    spec = finalize_vegalite_spec(spec, interactive=interactive,
                                  width=width, height=height)

    return Axes(spec, data=df)


def lag_plot(data, lag=1, **kwds):
    """Lag plot for time series.

    Parameters
    ----------
    data: pandas.Series
        the time series to plot
    lag: integer
        The lag of the scatter plot, default=1
    kwds:
        Additional keywords passed to data.vgplot.scatter

    Returns
    -------
    plot: VegaLite plot object
    """
    if lag != int(lag) or int(lag) <= 0:
        raise ValueError("lag must be a positive integer")
    lag = int(lag)

    values = data.values
    y1 = 'y(t)'
    y2 = 'y(t + {0})'.format(lag)
    lags = pd.DataFrame({y1: values[:-lag].T.ravel(),
                         y2: values[lag:].T.ravel()})
    if isinstance(data, pd.DataFrame):
        lags['variable'] = np.repeat(data.columns, lags.shape[0] / data.shape[1])
        kwds['c'] = 'variable'
    return lags.vgplot.scatter(y1, y2, **kwds)
