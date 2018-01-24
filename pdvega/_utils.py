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
