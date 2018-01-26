import warnings

import numpy as np
import pandas as pd

from ._utils import infer_vegalite_type
from ._pandas_internals import (FramePlotMethods,
                                SeriesPlotMethods,
                                register_dataframe_accessor,
                                register_series_accessor)


from vega3 import Vega, VegaLite

class VegaLitePlot(object):
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


class VegaLinePlot(VegaLitePlot):
    kind = 'line'
    def frame_plot(self, data, x=None, y=None, alpha=None,
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
                },
            },
        }
        if alpha is not None:
            assert 0 <= alpha <= 1
            spec['encoding']['opacity'] = {'value': alpha}

        spec = self.vgl_spec(spec, interactive=interactive,
                             width=width, height=height)
        return VegaLite(spec, data=df)

    def series_plot(self, data, alpha=None,
                    interactive=True, width=450, height=300, **kwds):
        self._warn_if_unused_keywords(kwds)
        df = data.reset_index()
        df.columns = map(str, df.columns)
        x, y = df.columns

        spec = {
          "mark": "line",
          "encoding": {
            "x": {"field": x, "type": infer_vegalite_type(df[x])},
            "y": {"field": y, "type": infer_vegalite_type(df[y])},
          }
        }

        if alpha is not None:
            assert 0 <= alpha <= 1
            spec['encoding']['opacity'] = {'value': alpha}

        spec = self.vgl_spec(spec, interactive=interactive,
                             width=width, height=height)
        return VegaLite(spec, data=df)


class VegaScatterPlot(VegaLitePlot):
    kind = 'scatter'

    def frame_plot(self, data, x, y, c=None, s=None, alpha=None,
                   interactive=True, width=450, height=300, **kwds):
        self._warn_if_unused_keywords(kwds)
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

        if alpha is not None:
            assert 0 <= alpha <= 1
            encoding['opacity'] = {'value': alpha}

        spec = {
          "mark": "circle",
          "encoding": encoding
        }

        spec = self.vgl_spec(spec, interactive=interactive,
                             width=width, height=height)
        return VegaLite(spec, data=data[cols])


class VegaAreaPlot(VegaLitePlot):
    kind = 'area'

    def frame_plot(self, data, x=None, y=None, stacked=True, alpha=None,
                   var_name='variable', value_name='value',
                   interactive=True, width=450, height=300, **kwds):
        self._warn_if_unused_keywords(kwds)

        usecols = [y] if y else None
        df = self._melt_frame(data, index=x, usecols=usecols,
                              var_name=var_name, value_name=value_name)
        x = df.columns[0]

        spec = {
          "mark": "area",
          "encoding": {
            "x": {
              "field": x,
              "type": infer_vegalite_type(df[x])
            },
            "y": {
              "field": value_name,
              "type": infer_vegalite_type(df[value_name]),
              "stack": 'zero' if stacked else None
            },
            "color": {
              "field": var_name,
              "type": infer_vegalite_type(df[var_name], ordinal_threshold=10)
            }
          }
        }

        if alpha is None and not stacked and df[var_name].nunique() > 1:
            alpha = 0.7

        if alpha is not None:
            assert 0 <= alpha <= 1
            spec['encoding']['opacity'] = {'value': alpha}

        spec = self.vgl_spec(spec, interactive=interactive,
                             width=width, height=height)

        return VegaLite(spec, data=df)

    def series_plot(self, data, interactive=True, width=450, height=300, alpha=None,
                    **kwds):
        self._warn_if_unused_keywords(kwds)
        df = data.reset_index()
        df.columns = map(str, df.columns)
        x, y = df.columns

        spec = {
          "mark": "area",
          "encoding": {
            "x": {"field": x, "type": infer_vegalite_type(df[x])},
            "y": {"field": y, "type": infer_vegalite_type(df[y])},
          },
        }

        if alpha is not None:
            assert 0 <= alpha <= 1
            spec['encoding']['opacity'] = {'value': alpha}

        spec = self.vgl_spec(spec, interactive=interactive,
                             width=width, height=height)

        return VegaLite(spec, data=df)


class VegaBarPlot(VegaLitePlot):
    kind = 'bar'

    def frame_plot(self, data, x, y, stacked=False, alpha=None,
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
          "mark": "bar",
          "encoding": {
            "x": {
                "field": x,
                "type": infer_vegalite_type(df[x], ordinal_threshold=50)
            },
            "y": {
                "field": "value",
                "type": infer_vegalite_type(df["value"]),
                "stack": 'zero' if stacked else None
            },
            "color": {
                "field": "variable",
                "type": infer_vegalite_type(df["variable"])
            },
          },
        }

        if alpha is None and not stacked and df[var_name].nunique() > 1:
            alpha = 0.7

        if alpha is not None:
            assert 0 <= alpha <= 1
            spec['encoding']['opacity'] = {'value': alpha}

        spec = self.vgl_spec(spec, interactive=interactive,
                             width=width, height=height)
        return VegaLite(spec, data=df)

    def series_plot(self, data, alpha=None, interactive=True,
                    width=450, height=300, **kwds):
        self._warn_if_unused_keywords(kwds)
        df = data.reset_index()
        df.columns = map(str, df.columns)
        x, y = df.columns

        spec = {
          "mark": "bar",
          "encoding": {
            "x": {
                "field": x,
                "type": infer_vegalite_type(df[x], ordinal_threshold=50)
            },
            "y": {
                "field": y,
                "type": infer_vegalite_type(df[y])
            },
          },
        }

        if alpha is not None:
            assert 0 <= alpha <= 1
            spec['encoding']['opacity'] = {'value': alpha}

        spec = self.vgl_spec(spec, interactive=interactive,
                             width=width, height=height)
        return VegaLite(spec, data=df)


class VegaBarhPlot(VegaBarPlot):
    kind = 'barh'

    def frame_plot(self, *args, **kwargs):
        plot = super(VegaBarhPlot, self).frame_plot(*args, **kwargs)
        enc = plot.spec['encoding']
        enc['x'], enc['y'] = enc['y'], enc['x']
        return plot

    def series_plot(self, *args, **kwargs):
        plot = super(VegaBarhPlot, self).series_plot(*args, **kwargs)
        enc = plot.spec['encoding']
        enc['x'], enc['y'] = enc['y'], enc['x']
        return plot


class VegaHistPlot(VegaLitePlot):
    kind = 'hist'

    def frame_plot(self, data, by=None, bins=10, stacked=False, alpha=None,
                   var_name='variable', value_name='value',
                   interactive=True, width=450, height=300, **kwds):
        self._warn_if_unused_keywords(kwds)
        if by is not None:
            raise NotImplementedError('vgplot.hist `by` keyword')
        df = data.melt(var_name='variable', value_name='value')

        spec = {
            "mark": "bar",
            "encoding": {
                "x": {
                    "bin": {"maxbins": bins},
                    "field": value_name,
                    "type": "quantitative"
                },
                "y": {
                    "aggregate": "count",
                    "type": "quantitative",
                    "stack": ('zero' if stacked else None)
                },
                "color": {
                    "field": var_name,
                    "type": "nominal"
                },
            },
        }

        if alpha is None and not stacked and df[var_name].nunique() > 1:
            alpha = 0.7

        if alpha is not None:
            assert 0 <= alpha <= 1
            spec['encoding']['opacity'] = {'value': alpha}

        spec = self.vgl_spec(spec, interactive=interactive,
                             width=width, height=height)
        return VegaLite(spec, data=df)

    def series_plot(self, data, bins=10, alpha=None, interactive=True,
                    width=450, height=300, **kwds):
        self._warn_if_unused_keywords(kwds)
        df = data.to_frame()
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
        }

        if alpha is not None:
            assert 0 <= alpha <= 1
            spec['encoding']['opacity'] = {'value': alpha}

        spec = self.vgl_spec(spec, interactive=interactive,
                             width=width, height=height)
        return VegaLite(spec, data=df)


class VegaHexbinPlot(VegaLitePlot):
    kind = 'hexbin'

    def frame_plot(self, data, x, y, C=None, reduce_C_function=None,
                   gridsize=100, alpha=None,
                   interactive=True, width=450, height=300, **kwds):
        # TODO: Use actual hexbins rather than a grid heatmap
        self._warn_if_unused_keywords(kwds)

        if reduce_C_function is not None:
            raise NotImplementedError("Custom reduce_C_function in hexbin")
        if C is None:
            df = data[[x, y]]
        else:
            df = data[[x, y, C]]

        spec = {
          "mark": "rect",
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
        }

        if alpha is not None:
            assert 0 <= alpha <= 1
            spec['encoding']['opacity'] = {'value': alpha}

        spec = self.vgl_spec(spec, interactive=interactive,
                             width=width, height=height)
        return VegaLite(spec, data=df)


class VegaKDEPlot(VegaLitePlot):
    kind = 'kde'

    def frame_plot(self, data, y=None, bw_method=None, alpha=None,
                   interactive=True, width=450, height=300, **kwds):
        from scipy.stats import gaussian_kde as kde

        if y is not None:
            df = data[y].to_frame()
        else:
            df = data

        tmin, tmax = df.min().min(), df.max().max()
        trange = tmax - tmin
        t = np.linspace(tmin - 0.5 * trange, tmax + 0.5 * trange, 1000)

        kde_df = pd.DataFrame({col: kde(df[col], bw_method=bw_method).evaluate(t)
                               for col in df}, index=t)
        kde_df.index.name = ' '

        return VegaLinePlot().frame_plot(kde_df, value_name='Density',
                                         alpha=alpha, interactive=interactive,
                                         width=width, height=height, **kwds)

    def series_plot(self, data, bw_method=None, alpha=None,
                    interactive=True, width=450, height=300, **kwds):
        from scipy.stats import gaussian_kde

        tmin, tmax = data.min(), data.max()
        trange = tmax - tmin
        t = np.linspace(tmin - 0.5 * trange, tmax + 0.5 * trange, 1000)

        kde_ser = pd.Series(gaussian_kde(data, bw_method=bw_method).evaluate(t),
                            index=t, name=data.name)
        kde_ser.index.name = ' '
        return VegaLinePlot().series_plot(kde_ser, alpha=alpha,
                                          interactive=interactive,
                                          width=width, height=height, **kwds)


@register_dataframe_accessor('vgplot')
class FrameVgPlotMethods(FramePlotMethods):
    def __call__(self, x=None, y=None,
                 kind='line', interactive=True,
                 width=450, height=300, **kwds):
        if kind == 'line':
            return VegaLinePlot().frame_plot(self._data, x=x, y=y,
                                             interactive=interactive,
                                             width=width, height=height, **kwds)
        elif kind == 'scatter':
            return VegaScatterPlot().frame_plot(self._data, x=x, y=y,
                                                interactive=interactive,
                                                width=width, height=height, **kwds)
        elif kind == 'area':
            return VegaAreaPlot().frame_plot(self._data, x=x, y=y,
                                             interactive=interactive,
                                             width=width, height=height, **kwds)
        elif kind == 'bar':
            return VegaBarPlot().frame_plot(self._data, x=x, y=y,
                                            interactive=interactive,
                                            width=width, height=height, **kwds)
        elif kind == 'barh':
            return VegaBarhPlot().frame_plot(self._data, x=x, y=y,
                                             interactive=interactive,
                                             width=width, height=height, **kwds)
        elif kind == 'hist':
            return VegaHistPlot().frame_plot(self._data, interactive=interactive,
                                             width=width, height=height, **kwds)
        elif kind == 'hexbin':
            return VegaHexbinPlot().frame_plot(self._data, x=x, y=y,
                                               interactive=interactive,
                                               width=width, height=height, **kwds)
        elif kind in ['kde', 'density']:
            return VegaKDEPlot().frame_plot(self._data, y=y,
                                            interactive=interactive,
                                            width=width, height=height, **kwds)
        else:
            raise NotImplementedError("kind = {0}".format(kind))


@register_series_accessor('vgplot')
class SeriesVgPlotMethods(SeriesPlotMethods):
    def __call__(self, kind='line', interactive=True, width=450, height=300,
                 **kwds):
        if kind == 'line':
            return VegaLinePlot().series_plot(self._data, interactive=interactive,
                                              width=width, height=height, **kwds)
        elif kind == 'area':
            return VegaAreaPlot().series_plot(self._data, interactive=interactive,
                                              width=width, height=height, **kwds)
        elif kind == 'bar':
            return VegaBarPlot().series_plot(self._data, interactive=interactive,
                                             width=width, height=height, **kwds)
        elif kind == 'barh':
            return VegaBarhPlot().series_plot(self._data, interactive=interactive,
                                              width=width, height=height, **kwds)
        elif kind == 'hist':
            return VegaHistPlot().series_plot(self._data, interactive=interactive,
                                              width=width, height=height, **kwds)
        elif kind in ['kde', 'density']:
            return VegaKDEPlot().series_plot(self._data, interactive=interactive,
                                             width=width, height=height, **kwds)
        else:
            raise NotImplementedError("kind = {0}".format(kind))
