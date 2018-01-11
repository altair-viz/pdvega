from ._utils import unstack_cols
from pandas.plotting._core import FramePlotMethods, SeriesPlotMethods
from vega import Vega, VegaLite


def vgplot_line(df, x=None, y=None):
    if x is None:
        if df.index.name is None:
            df.index.name = 'index'
        x = df.index.name
        df = df.reset_index()
    assert x in df.columns

    if y is not None:
        assert y in df.columns
        df = df[[x, y]]

    df = df.melt([x], var_name='variable', value_name='value')

    D = {
      "$schema": "https://vega.github.io/schema/vega-lite/v2.json",
      "mark": "line",
      "encoding": {
        "x": {"field": x, "type": "quantitative"},
        "y": {"field": "value", "type": "quantitative"},
        "color": {"field": "variable", "type": "nominal"}
      }
    }
    return VegaLite(D, data=df)

def vgplot_scatter(df, x, y):
    assert x in df.columns
    assert y in df.columns

    df = df[[x, y]]
    D = {
      "$schema": "https://vega.github.io/schema/vega-lite/v2.json",
      "mark": "circle",
      "encoding": {
        "x": {"field": x, "type": "quantitative"},
        "y": {"field": y, "type": "quantitative"},
      }
    }
    return VegaLite(D, data=df)

def vgplot_bar(df, x, y):
    if x is None:
        if df.index.name is None:
            df.index.name = 'index'
        x = df.index.name
        df = df.reset_index()
    assert x in df.columns

    if y is not None:
        assert y in df.columns
        df = df[[x, y]]

    df = df.melt([x], var_name='variable', value_name='value')

    D = {
      "$schema": "https://vega.github.io/schema/vega-lite/v2.json",
      "mark": "bar",
      "encoding": {
        "x": {"field": x, "type": "ordinal"},
        "y": {"field": "value", "type": "quantitative"},
        "color": {"field": "variable", "type": "nominal"}
      }
    }
    return VegaLite(D, data=df)


class FrameVgPlotMethods(FramePlotMethods):
    def __call__(self, x=None, y=None, kind='line', ax=None,
                 subplots=False, sharex=None, sharey=False, layout=None,
                 figsize=None, use_index=True, title=None, grid=None,
                 legend=True, style=None, logx=False, logy=False, loglog=False,
                 xticks=None, yticks=None, xlim=None, ylim=None,
                 rot=None, fontsize=None, colormap=None, table=False,
                 yerr=None, xerr=None,
                 secondary_y=False, sort_columns=False, **kwds):
        if kind == 'line':
            return vgplot_line(self._data, x=x, y=y)
        elif kind == 'scatter':
            return vgplot_scatter(self._data, x=x, y=y)
        elif kind == 'bar':
            return vgplot_bar(self._data, x=x, y=y)
        else:
            raise NotImplementedError("kind = {0}".format(kind))


class SeriesVgPlotMethods(SeriesPlotMethods):
    def __call__(self, kind='line', ax=None,
                 figsize=None, use_index=True, title=None, grid=None,
                 legend=False, style=None, logx=False, logy=False,
                 loglog=False, xticks=None, yticks=None,
                 xlim=None, ylim=None,
                 rot=None, fontsize=None, colormap=None, table=False,
                 yerr=None, xerr=None,
                 label=None, secondary_y=False, **kwds):
        if kind == 'line':
            return plot_line(self._data.to_frame())
        else:
            raise NotImplementedError("kind = {0}".format(kind))
