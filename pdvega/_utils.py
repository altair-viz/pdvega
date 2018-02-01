import warnings

import pandas as pd

from ._pandas_internals import infer_dtype as pd_infer_dtype


def infer_vegalite_type(data, ordinal_threshold=6):
    """
    From an array-like input, infer the correct vega typecode
    ('ordinal', 'nominal', 'quantitative', or 'temporal')

    Parameters
    ----------
    data: Numpy array or Pandas Series
        data for which the type will be inferred
    ordinal_threshold: integer (default: 0)
        integer data will result in a 'quantitative' type, unless the
        number of unique values is smaller than ordinal_threshold.

    Adapted from code at http://github.com/altair-viz/altair/
    Licence: BSD-3
    """
    # infer based on the dtype of the input
    typ = pd_infer_dtype(data)

    # TODO: Once this returns 'O', please update test_select_x and test_select_y in test_api.py

    if typ in ['mixed-integer', 'integer']:
        if ordinal_threshold and pd.Series(data).nunique() <= ordinal_threshold:
            return 'ordinal'
        else:
            return 'quantitative'
    elif typ in ['floating', 'mixed-integer-float', 'complex']:
        return 'quantitative'
    elif typ in ['string', 'bytes', 'categorical', 'boolean', 'mixed', 'unicode']:
        return 'nominal'
    elif typ in ['datetime', 'datetime64', 'timedelta',
                 'timedelta64', 'date', 'time', 'period']:
        return 'temporal'
    else:
        warnings.warn("I don't know how to infer vegalite type from '{0}'.  "
                      "Defaulting to nominal.".format(typ))
        return 'nominal'


def unpivot_frame(frame, x=None, y=None,
                  var_name='variable', value_name='value'):
    """Unpivot a dataframe for use with Vega/Vega-Lite

    The input is a frame with any number of columns,
    output is a frame with three columns: x value, y values,
    and variable names.
    """
    if x is None:
        cols = frame.columns
        frame = frame.reset_index()
        x = (set(frame.columns) - set(cols)).pop()
    # frame.melt doesn't properly check for nonexisting columns, so we
    # start by indexing here. Tuples of column names also need to be
    # converted to lists for checking indexing
    if isinstance(x, tuple):
        x = list(x)
    if isinstance(y, tuple):
        y = list(y)
    if x is not None:
        _ = frame[x]
    if y is not None:
        _ = frame[y]
    return frame.melt(id_vars=x, value_vars=y,
                      var_name=var_name, value_name=value_name)


def warn_if_keywords_unused(kind, kwds):
    if kwds:
        if len(kwds) == 1:
            keys = tuple(kwds.keys())[0]
        else:
            keys = tuple(kwds.keys())
        warnings.warn("Unrecognized keywords in vgplot.{0}(): {1}"
                      "".format(kind, repr(keys)))


def finalize_vegalite_spec(spec, interactive=True, width=450, height=300):
    spec.update({
        "$schema": "https://vega.github.io/schema/vega-lite/v2.json",
        "width": width,
        "height": height
    })
    if interactive:
        spec.update({
            "selection": {
                "grid": {
                    "type": "interval",
                    "bind": "scales"
                }
            }
        })
    return spec
