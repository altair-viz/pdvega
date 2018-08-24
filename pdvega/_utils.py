import warnings
import altair as alt
import numpy as np
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

    if typ in ('mixed-integer', 'integer'):
        if ordinal_threshold and pd.Series(data).nunique() <= ordinal_threshold:
            return 'ordinal'
        else:
            return 'quantitative'
    elif typ in ('floating', 'mixed-integer-float', 'complex'):
        return 'quantitative'
    elif typ in ('string', 'bytes', 'categorical', 'boolean', 'mixed', 'unicode', 'object'):
        return 'nominal'
    elif typ in ('datetime', 'datetime64', 'timedelta',
                 'timedelta64', 'date', 'time', 'period'):
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
        _ = frame[x] # flake8: noqa
    if y is not None:
        _ = frame[y] # flake8: noqa
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


def validate_aggregation(agg):
    """Validate an aggregation for use in Vega-Lite.

    Translate agg to one of the following supported named aggregations:
    ['mean', 'sum', 'median', 'min', 'max', 'count']

    Parameters
    ----------
    agg : string or callable
        A string

    Supported reductions are ['mean', 'sum', 'median', 'min', 'max', 'count'].

    If agg is a numpy function, the return value is the string representation.

    If agg is unrecognized, raise a ValueError
    """
    if agg is None:
        return agg
    supported_aggs = ['mean', 'sum', 'median', 'min', 'max', 'count']
    numpy_aggs = {getattr(np, a): a
                  for a in ['mean', 'sum', 'median', 'min', 'max']}
    builtin_aggs = {min: 'min', max: 'max', sum: 'sum'}

    agg = numpy_aggs.get(agg, agg)
    agg = builtin_aggs.get(agg, agg)

    if agg not in supported_aggs:
        raise ValueError("Unrecognized Vega-Lite aggregation: {0}".format(agg))

    return agg
