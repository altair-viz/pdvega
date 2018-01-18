
try:
    from pandas.api.types import infer_dtype as pd_infer_dtype
except ImportError: # Pandas before 0.20.0
    from pandas.lib import infer_dtype as pd_infer_dtype


def infer_vegalite_type(data):
    """
    From an array-like input, infer the correct vega typecode
    ('ordinal', 'nominal', 'quantitative', or 'temporal')

    Parameters
    ----------
    data: Numpy array or Pandas Series

    Adapted from code at http://github.com/altair-viz/altair/
    Licence: BSD-3
    """
    # infer based on the dtype of the input
    typ = pd_infer_dtype(data)

    # TODO: Once this returns 'O', please update test_select_x and test_select_y in test_api.py

    if typ in ['floating', 'mixed-integer-float', 'integer',
               'mixed-integer', 'complex']:
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


def unstack_cols(df):
    cols = df.columns
    df = df.reset_index()
    return df.melt(['index'],
                   value_vars=cols,
                   var_name='variable',
                   value_name='value')
