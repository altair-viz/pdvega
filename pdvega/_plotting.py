from ._utils import unstack_cols, infer_vegalite_type
from pandas.plotting._core import FramePlotMethods, SeriesPlotMethods
from vega3 import Vega, VegaLite


INTERACTIVE_SCALES = {
    "selection": {
        "grid": {
            "type": "interval", "bind": "scales"
        }
    }
}


def vgplot_line(df, x=None, y=None, interactive=True, width=450, height=300):
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
        "x": {"field": x, "type": infer_vegalite_type(df[x])},
        "y": {"field": "value", "type": infer_vegalite_type(df["value"])},
        "color": {"field": "variable", "type": infer_vegalite_type(df["variable"], ordinal_threshold=10)}
      },
      "width": width,
      "height": height
    }

    if interactive:
        D.update(INTERACTIVE_SCALES)

    return VegaLite(D, data=df)


def vgplot_scatter(df, x, y, c=None, s=None,
                   interactive=True, width=450, height=300):
    cols = [x, y]
    assert x in df.columns
    assert y in df.columns

    D = {
      "$schema": "https://vega.github.io/schema/vega-lite/v2.json",
      "mark": "circle",
      "encoding": {
        "x": {"field": x, "type": infer_vegalite_type(df[x])},
        "y": {"field": y, "type": infer_vegalite_type(df[y])},
      },
      "width": width,
      "height": height
    }

    if c is not None:
        assert c in df.columns
        cols.append(c)
        D['encoding']['color'] = {'field': c, 'type': infer_vegalite_type(df[c])}

    if s is not None:
        assert s in df.columns
        cols.append(s)
        D['encoding']['size'] = {'field': s, 'type': infer_vegalite_type(df[s])}

    if interactive:
        D.update(INTERACTIVE_SCALES)

    df = df[cols]
    return VegaLite(D, data=df)


def vgplot_bar(df, x, y, stacked=False, interactive=True, width=450, height=300):
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
        "x": {"field": x, "type": infer_vegalite_type(df[x], ordinal_threshold=50)},
        "y": {"field": "value", "type": infer_vegalite_type(df["value"])},
        "color": {"field": "variable", "type": infer_vegalite_type(df["variable"])},
      },
      "width": width,
      "height": height,
    }

    if stacked:
        D['encoding']['y']['stack'] = 'zero'
    else:
        D['encoding']['y']['stack'] = None
        D['encoding']['opacity'] = {"value": 0.7}

    if interactive:
        D.update(INTERACTIVE_SCALES)

    return VegaLite(D, data=df)


def vgplot_barh(df, x, y, stacked=False, interactive=True, width=450, height=300):
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
        "x": {"field": "value", "type": infer_vegalite_type(df["value"])},
        "y": {"field": x, "type": infer_vegalite_type(df[x], ordinal_threshold=50)},
        "color": {"field": "variable", "type": infer_vegalite_type(df["variable"])},
      },
      "width": width,
      "height": height,
    }

    if stacked:
        D['encoding']['x']['stack'] = 'zero'
    else:
        D['encoding']['x']['stack'] = None
        D['encoding']['opacity'] = {"value": 0.7}

    if interactive:
        D.update(INTERACTIVE_SCALES)

    return VegaLite(D, data=df)


def vgplot_area(df, x=None, y=None, stacked=True,
                interactive=True, width=450, height=300):
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
      "mark": "area",
      "encoding": {
        "x": {"field": x, "type": infer_vegalite_type(df[x])},
        "y": {"field": "value", "type": infer_vegalite_type(df["value"])},
        "color": {"field": "variable", "type": infer_vegalite_type(df["variable"], ordinal_threshold=10)}
      },
      "width": width,
      "height": height
    }

    if stacked:
        D['encoding']['y']['stack'] = 'zero'
    else:
        D['encoding']['y']['stack'] = None
        D['encoding']['opacity'] = {'value': 0.7}

    if interactive:
        D.update(INTERACTIVE_SCALES)

    return VegaLite(D, data=df)


class FrameVgPlotMethods(FramePlotMethods):
    def __call__(self, x=None, y=None,
                 kind='line', interactive=True,
                 width=450, height=300, **kwds):
        if kind == 'line':
            return vgplot_line(self._data, x=x, y=y, interactive=interactive,
                               width=width, height=height, **kwds)
        elif kind == 'scatter':
            return vgplot_scatter(self._data, x=x, y=y, interactive=interactive,
                                  width=width, height=height, **kwds)
        elif kind == 'bar':
            return vgplot_bar(self._data, x=x, y=y, interactive=interactive,
                              width=width, height=height, **kwds)
        elif kind == 'barh':
            return vgplot_barh(self._data, x=x, y=y, interactive=interactive,
                               width=width, height=height, **kwds)
        elif kind == 'area':
            return vgplot_area(self._data, x=x, y=y, interactive=interactive,
                               width=width, height=height, **kwds)
        else:
            raise NotImplementedError("kind = {0}".format(kind))


class SeriesVgPlotMethods(SeriesPlotMethods):
    def __call__(self, kind='line', interactive=True, width=450, height=300,
                 **kwds):
        if kind == 'line':
            return plot_line(self._data.to_frame(), interactive=interactive,
                             width=width, height=height, **kwds)
        else:
            raise NotImplementedError("kind = {0}".format(kind))
