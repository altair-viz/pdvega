"""Core plotting routines"""
import warnings

from vega3 import VegaLite

from ._utils import infer_vegalite_type


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
    pandas.plotting.scatter_matrix
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
          "x": {"field": {"repeat": "column"},"type": "quantitative"},
          "y": {"field": {"repeat": "row"},"type": "quantitative"},
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
    return VegaLite(spec, data=frame)
