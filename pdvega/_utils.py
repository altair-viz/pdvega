def unstack_cols(df):
    cols = df.columns
    df = df.reset_index()
    return df.melt(['index'],
                   value_vars=cols,
                   var_name='variable',
                   value_name='value')
