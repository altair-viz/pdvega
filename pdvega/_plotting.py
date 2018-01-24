import warnings

import numpy as np
import pandas as pd

from ._utils import infer_vegalite_type
from ._pandas_internals import FramePlotMethods, SeriesPlotMethods
from vega3 import Vega, VegaLite


INTERACTIVE_SCALES = {
    "selection": {
        "grid": {
            "type": "interval", "bind": "scales"
        }
    }
}

class VGLPlot(object):
    kind = None

    def _warn_if_unused_keywords(self, kwds):
        if kwds:
            warnings.warn("Unrecognized keywords in vgplot.{0}(): {1}"
                          "".format(self.kind, list(kwds.keys())))

    @staticmethod
    def _melt_frame(df, index=None, usecols=None,
                    var_name='variable', value_name='value'):
        if index is None:
            cols = df.columns
            df = df.reset_index()
            index = (set(df.columns) - set(cols)).pop()
        assert index in df.columns
        if usecols:
            df = df[[index] + list(usecols)]
        return df.melt([index], var_name=var_name, value_name=value_name)

    def vgl_spec(self, spec, interactive=True, width=450, height=300):
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

    def frame_plot(self, *args, **kwargs):
        raise NotImplementedError("kind='{0}' for dataframe".format(self.kind))

    def series_plot(self, *args, **kwargs):
        raise NotImplementedError("kind='{0}' for series".format(self.kind))


class VgLinePlot(VGLPlot):
    kind = 'line'
    def frame_plot(self, data, x=None, y=None,
                   var_name='variable', value_name='value',
                   interactive=True, width=450, height=300, **kwds):
        self._warn_if_unused_keywords(kwds)

        if y:
            usecols = [y]
        else:
            usecols = None
        df = self._melt_frame(data, index=x, usecols=usecols,
                              var_name=var_name, value_name=value_name)
        x = df.columns[0]

        spec = {
            "mark": "line",
            "encoding": {
                "x": {
                    "field": x,
                    "type": infer_vegalite_type(df[x])
                },
                "y": {
                    "field": value_name,
                    "type": infer_vegalite_type(df[value_name])
                },
                "color": {
                    "field": var_name,
                    "type": infer_vegalite_type(df[var_name],
                                                ordinal_threshold=10)
                }
            },
        }
        spec = self.vgl_spec(spec, interactive=interactive,
                             width=width, height=height)
        return VegaLite(spec, data=df)

    def series_plot(self, data, interactive=True, width=450, height=300, **kwds):
        self._warn_if_unused_keywords(kwds)
        df = data.reset_index()
        df.columns = map(str, df.columns)
        x, y = df.columns

        spec = self.vgl_spec({
          "mark": "line",
          "encoding": {
            "x": {"field": x, "type": infer_vegalite_type(df[x])},
            "y": {"field": y, "type": infer_vegalite_type(df[y])},
          }
        })

        spec = self.vgl_spec(spec, interactive=interactive,
                             width=width, height=height)
        return VegaLite(spec, data=df)


class VgScatterPlot(VGLPlot):
    kind = 'scatter'

    def frame_plot(self, data, x, y, c=None, s=None,
                   interactive=True, width=450, height=300):
        cols = [x, y]

        encoding = {
          "x": {"field": x, "type": infer_vegalite_type(data[x])},
          "y": {"field": y, "type": infer_vegalite_type(data[y])},
        }

        if c is not None:
            cols.append(c)
            encoding['color'] = {
                'field': c,
                'type': infer_vegalite_type(data[c])
            }

        if s is not None:
            cols.append(s)
            encoding['size'] = {
                'field': s,
                'type': infer_vegalite_type(data[s])
            }

        spec = {
          "mark": "circle",
          "encoding": encoding
        }


        spec = self.vgl_spec(spec, interactive=interactive,
                             width=width, height=height)
        return VegaLite(spec, data=data[cols])


def vgplot_series_area(ser, interactive=True, width=450, height=300):
    df = ser.reset_index()
    df.columns = map(str, df.columns)
    x, y = df.columns

    D = {
      "$schema": "https://vega.github.io/schema/vega-lite/v2.json",
      "mark": "area",
      "encoding": {
        "x": {"field": x, "type": infer_vegalite_type(df[x])},
        "y": {"field": y, "type": infer_vegalite_type(df[y])},
      },
      "width": width,
      "height": height
    }

    if interactive:
        D.update(INTERACTIVE_SCALES)

    return VegaLite(D, data=df)


def vgplot_df_bar(df, x, y, stacked=False, interactive=True, width=450, height=300):
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


def vgplot_series_bar(ser, interactive=True, width=450, height=300):
    df = ser.reset_index()
    df.columns = map(str, df.columns)
    x, y = df.columns

    D = {
      "$schema": "https://vega.github.io/schema/vega-lite/v2.json",
      "mark": "bar",
      "encoding": {
        "x": {"field": x, "type": infer_vegalite_type(df[x], ordinal_threshold=50)},
        "y": {"field": y, "type": infer_vegalite_type(df[y])},
      },
      "width": width,
      "height": height,
    }

    if interactive:
        D.update(INTERACTIVE_SCALES)

    return VegaLite(D, data=df)


def vgplot_df_barh(df, x, y, stacked=False, interactive=True, width=450, height=300):
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


def vgplot_series_barh(ser, interactive=True, width=450, height=300):
    df = ser.reset_index()
    df.columns = map(str, df.columns)
    x, y = df.columns

    D = {
      "$schema": "https://vega.github.io/schema/vega-lite/v2.json",
      "mark": "bar",
      "encoding": {
        "x": {"field": y, "type": infer_vegalite_type(df[y])},
        "y": {"field": x, "type": infer_vegalite_type(df[x], ordinal_threshold=50)}
      },
      "width": width,
      "height": height,
    }

    if interactive:
        D.update(INTERACTIVE_SCALES)

    return VegaLite(D, data=df)


def vgplot_df_area(df, x=None, y=None, stacked=True,
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


def vgplot_df_hist(df, by=None, bins=10, stacked=False,
                   interactive=True, width=450, height=300):
    if by is not None:
        raise NotImplementedError('vgplot.hist `by` keyword')
    df = df.melt(var_name='variable', value_name='value')

    spec = {
        "mark": "bar",
        "encoding": {
            "x": {
                "bin": {"maxbins": bins},
                "field": "value",
                "type": "quantitative"
            },
            "y": {
                "aggregate": "count",
                "type": "quantitative",
                "stack": ('zero' if stacked else None)
            },
            "color": {
                "field": "variable",
                "type": "nominal"
            },
        },
        "width": width,
        "height": height
    }

    if interactive:
        spec.update(INTERACTIVE_SCALES)

    return VegaLite(spec, data=df)


def vgplot_series_hist(ser, bins=10, interactive=True,
                       width=450, height=300):
    df = ser.to_frame()
    df.columns = map(str, df.columns)

    spec = {
        "mark": "bar",
        "encoding": {
            "x": {
                "bin": {"maxbins": bins},
                "field": df.columns[0],
                "type": "quantitative"
            },
            "y": {
                "aggregate": "count",
                "type": "quantitative"
            }
        },
        "width": width,
        "height": height
    }

    if interactive:
        spec.update(INTERACTIVE_SCALES)

    return VegaLite(spec, data=df)


def vgplot_df_hexbin(df, x, y, C=None, reduce_C_function=None, gridsize=100,
                     interactive=True, width=450, height=300):
    # TODO: Use actual hexbins rather than a grid heatmap
    if reduce_C_function is not None:
        raise NotImplementedError("Custom reduce_C_function in hexbin")
    if C is None:
        df = df[[x, y]]
    else:
        df = df[[x, y, C]]

    spec = {
      "$schema": "https://vega.github.io/schema/vega-lite/v2.json",
      "encoding": {
        "x": {"field": x, "bin": {"maxbins": gridsize}, "type": "quantitative"},
        "y": {"field": y, "bin": {"maxbins": gridsize}, "type": "quantitative"},
        "color": ({"aggregate": "count", "type": "quantitative"} if C is None else
                  {"field": C, "aggregate": "mean", "type": "quantitative"})
      },
      "config": {
        "range": {
          "heatmap": {
            "scheme": "greenblue"
          }
        },
        "view": {
          "stroke": "transparent"
        }
      },
      "mark": "rect",
      "width": width,
      "height": height,
    }

    if interactive:
        spec.update(INTERACTIVE_SCALES)

    return VegaLite(spec, data=df)


def vgplot_df_kde(df, y=None, bw_method=None, interactive=True,
                  width=450, height=300):
    from scipy.stats import gaussian_kde

    if y is not None:
        df = df[y].to_frame()

    tmin, tmax = df.min().min(), df.max().max()
    trange = tmax - tmin
    t = np.linspace(tmin - 0.5 * trange, tmax + 0.5 * trange, 1000)

    kde_df = pd.DataFrame({col: gaussian_kde(df[col], bw_method=bw_method).evaluate(t)
                           for col in df}, index=t)
    kde_df.index.name = ' '

    return VgLinePlot().frame_plot(kde_df, value_name='Density')


def vgplot_series_kde(ser, bw_method=None, interactive=True,
                      width=450, height=300):
    from scipy.stats import gaussian_kde

    tmin, tmax = ser.min(), ser.max()
    trange = tmax - tmin
    t = np.linspace(tmin - 0.5 * trange, tmax + 0.5 * trange, 1000)

    kde_ser = pd.Series(gaussian_kde(ser, bw_method=bw_method).evaluate(t),
                        index=t, name=ser.name)
    kde_ser.index.name = ' '
    return VgLinePlot().series_plot(kde_ser)


class FrameVgPlotMethods(FramePlotMethods):
    def __call__(self, x=None, y=None,
                 kind='line', interactive=True,
                 width=450, height=300, **kwds):
        if kind == 'line':
            return VgLinePlot().frame_plot(self._data, x=x, y=y,
                                           interactive=interactive,
                                           width=width, height=height, **kwds)
        elif kind == 'scatter':
            return VgScatterPlot().frame_plot(self._data, x=x, y=y,
                                              interactive=interactive,
                                              width=width, height=height, **kwds)
        elif kind == 'bar':
            return vgplot_df_bar(self._data, x=x, y=y, interactive=interactive,
                                 width=width, height=height, **kwds)
        elif kind == 'barh':
            return vgplot_df_barh(self._data, x=x, y=y, interactive=interactive,
                                  width=width, height=height, **kwds)
        elif kind == 'area':
            return vgplot_df_area(self._data, x=x, y=y, interactive=interactive,
                                  width=width, height=height, **kwds)
        elif kind == 'hist':
            return vgplot_df_hist(self._data, interactive=interactive,
                                  width=width, height=height, **kwds)
        elif kind == 'hexbin':
            return vgplot_df_hexbin(self._data, x=x, y=y, interactive=interactive,
                                    width=width, height=height, **kwds)
        elif kind in ['kde', 'density']:
            return vgplot_df_kde(self._data, y=y, interactive=interactive,
                                 width=width, height=height, **kwds)
        else:
            raise NotImplementedError("kind = {0}".format(kind))


class SeriesVgPlotMethods(SeriesPlotMethods):
    def __call__(self, kind='line', interactive=True, width=450, height=300,
                 **kwds):
        if kind == 'line':
            return VgLinePlot().series_plot(self._data, interactive=interactive,
                                            width=width, height=height, **kwds)
        elif kind == 'bar':
            return vgplot_series_bar(self._data, interactive=interactive,
                                 width=width, height=height, **kwds)
        elif kind == 'barh':
            return vgplot_series_barh(self._data, interactive=interactive,
                               width=width, height=height, **kwds)
        elif kind == 'area':
            return vgplot_series_area(self._data, interactive=interactive,
                                      width=width, height=height, **kwds)
        elif kind == 'hist':
            return vgplot_series_hist(self._data, interactive=interactive,
                                      width=width, height=height, **kwds)
        elif kind in ['kde', 'density']:
            return vgplot_series_kde(self._data, interactive=interactive,
                                     width=width, height=height, **kwds)
        else:
            raise NotImplementedError("kind = {0}".format(kind))
