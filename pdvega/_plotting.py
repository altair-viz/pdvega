import warnings

import numpy as np
import pandas as pd

from ._utils import infer_vegalite_type
from ._pandas_internals import (PandasObject,
                                register_dataframe_accessor,
                                register_series_accessor)



#################################################################
from ._axes import VegaLiteAxes

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


def _warn_if_unused_keywords(kind, kwds):
    if kwds:
        warnings.warn("Unrecognized keywords in vgplot.{0}(): {1}"
                      "".format(kind, list(kwds.keys())))


def _finalize_spec(spec, interactive=True, width=450, height=300):
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


class BasePlotMethods(PandasObject):
    def __init__(self, data):
        self._data = data

    def __call__(self, kind, *args, **kwargs):
        raise NotImplementedError()


@register_series_accessor('vgplot')
class SeriesPlotMethods(BasePlotMethods):
    def __call__(self, kind='line', **kwargs):
        try:
            plot_method = getattr(self, kind)
        except AttributeError:
            raise ValueError("kind='{0}' not valid for {1}"
                             "".format(kind, self.__class__.__name__))
        return plot_method(**kwargs)

    def line(self, alpha=None,
             interactive=True, width=450, height=300, **kwds):
        _warn_if_unused_keywords('line', kwds)
        data = self._data
        df = data.reset_index()
        df.columns = map(str, df.columns)
        x, y = df.columns

        spec = {
          "mark": "line",
          "encoding": {
            "x": {
                "field": x,
                "type": infer_vegalite_type(df[x], ordinal_threshold=0)
            },
            "y": {
                "field": y,
                "type": infer_vegalite_type(df[y], ordinal_threshold=0)
            },
          }
        }

        if alpha is not None:
            assert 0 <= alpha <= 1
            spec['encoding']['opacity'] = {'value': alpha}

        _finalize_spec(spec, width=width, height=height,
                       interactive=interactive)

        return VegaLiteAxes(spec, df)

    def area(self, interactive=True, width=450, height=300, alpha=None,
             **kwds):
        _warn_if_unused_keywords('area', kwds)
        df = self._data.reset_index()
        df.columns = map(str, df.columns)
        x, y = df.columns

        spec = {
          "mark": "area",
          "encoding": {
            "x": {
                "field": x,
                "type": infer_vegalite_type(df[x], ordinal_threshold=0)
            },
            "y": {
                "field": y,
                "type": infer_vegalite_type(df[y], ordinal_threshold=0)
            },
          },
        }

        if alpha is not None:
            assert 0 <= alpha <= 1
            spec['encoding']['opacity'] = {'value': alpha}

        spec = _finalize_spec(spec, interactive=interactive,
                              width=width, height=height)

        return VegaLiteAxes(spec, data=df)

    def bar(self, alpha=None, interactive=True,
            width=450, height=300, **kwds):
        _warn_if_unused_keywords('bar', kwds)

        df = self._data.reset_index()
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
                "type": infer_vegalite_type(df[y], ordinal_threshold=0)
            },
          },
        }

        if alpha is not None:
            assert 0 <= alpha <= 1
            spec['encoding']['opacity'] = {'value': alpha}

        spec = _finalize_spec(spec, interactive=interactive,
                              width=width, height=height)
        return VegaLiteAxes(spec, data=df)

    def barh(self, alpha=None, interactive=True,
             width=450, height=300, **kwds):
        plot = self.bar(alpha=alpha, interactive=interactive,
                        width=width, height=height, **kwds)
        enc = plot.spec['encoding']
        enc['x'], enc['y'] = enc['y'], enc['x']
        return plot

    def hist(self, bins=10, alpha=None, interactive=True,
             width=450, height=300, **kwds):
        _warn_if_unused_keywords('hist', kwds)
        df = self._data.to_frame()
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

        spec = _finalize_spec(spec, interactive=interactive,
                              width=width, height=height)
        return VegaLiteAxes(spec, data=df)

    def kde(self, bw_method=None, alpha=None,
            interactive=True, width=450, height=300, **kwds):
        from scipy.stats import gaussian_kde

        data = self._data
        tmin, tmax = data.min(), data.max()
        trange = tmax - tmin
        t = np.linspace(tmin - 0.5 * trange, tmax + 0.5 * trange, 1000)

        kde_ser = pd.Series(gaussian_kde(data, bw_method=bw_method).evaluate(t),
                            index=t, name=data.name)
        kde_ser.index.name = ' '
        f = self.__class__(kde_ser)
        return f.line(alpha=alpha, interactive=interactive,
                      width=width, height=height, **kwds)

    density = kde


@register_dataframe_accessor('vgplot')
class FramePlotMethods(BasePlotMethods):
    def __call__(self, x=None, y=None, kind='line', **kwargs):
        try:
            plot_method = getattr(self, kind)
        except AttributeError:
            raise ValueError("kind='{0}' not valid for {1}"
                             "".format(kind, self.__class__.__name__))
        return plot_method(x=x, y=y, **kwargs)

    def line(self, x=None, y=None, alpha=None,
             var_name='variable', value_name='value',
             interactive=True, width=450, height=300, **kwds):
        _warn_if_unused_keywords('line', kwds)
        data = self._data

        if y:
            usecols = [y]
        else:
            usecols = None
        df = _melt_frame(data, index=x, usecols=usecols,
                         var_name=var_name, value_name=value_name)
        x = df.columns[0]

        spec = {
            "mark": "line",
            "encoding": {
                "x": {
                    "field": x,
                    "type": infer_vegalite_type(df[x],
                                                ordinal_threshold=0)
                },
                "y": {
                    "field": value_name,
                    "type": infer_vegalite_type(df[value_name],
                                                ordinal_threshold=0)
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

        _finalize_spec(spec, width=width, height=height,
                       interactive=interactive)

        return VegaLiteAxes(spec, df)

    def scatter(self, x, y, c=None, s=None, alpha=None,
                interactive=True, width=450, height=300, **kwds):
        _warn_if_unused_keywords('scatter', kwds)
        data = self._data
        cols = [x, y]

        encoding = {
          "x": {
              "field": x,
              "type": infer_vegalite_type(data[x], ordinal_threshold=0)
          },
          "y": {
              "field": y,
              "type": infer_vegalite_type(data[y], ordinal_threshold=0)
          },
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

        spec = _finalize_spec(spec, interactive=interactive,
                              width=width, height=height)
        return VegaLiteAxes(spec, data=data[cols])

    def area(self, x=None, y=None, stacked=True, alpha=None,
             var_name='variable', value_name='value',
             interactive=True, width=450, height=300, **kwds):
        _warn_if_unused_keywords('area', kwds)
        data = self._data

        usecols = [y] if y else None
        df = _melt_frame(data, index=x, usecols=usecols,
                         var_name=var_name, value_name=value_name)
        x = df.columns[0]

        spec = {
          "mark": "area",
          "encoding": {
            "x": {
              "field": x,
              "type": infer_vegalite_type(df[x], ordinal_threshold=0)
            },
            "y": {
              "field": value_name,
              "type": infer_vegalite_type(df[value_name], ordinal_threshold=0),
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

        spec = _finalize_spec(spec, interactive=interactive,
                               width=width, height=height)

        return VegaLiteAxes(spec, data=df)

    def bar(self, x=None, y=None, stacked=False, alpha=None,
            var_name='variable', value_name='value',
            interactive=True, width=450, height=300, **kwds):
        _warn_if_unused_keywords('bar', kwds)

        if y:
            usecols = [y]
        else:
            usecols = None
        df = _melt_frame(self._data, index=x, usecols=usecols,
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
                "type": infer_vegalite_type(df["value"], ordinal_threshold=0),
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

        spec = _finalize_spec(spec, interactive=interactive,
                              width=width, height=height)
        return VegaLiteAxes(spec, data=df)

    def barh(self, x=None, y=None, stacked=False, alpha=None,
             var_name='variable', value_name='value',
             interactive=True, width=450, height=300, **kwds):
        plot = self.bar(x=x, y=y, stacked=stacked, alpha=alpha,
                        var_name=var_name, value_name=value_name,
                        interactive=interactive, width=width, height=height,
                        **kwds)
        enc = plot.spec['encoding']
        enc['x'], enc['y'] = enc['y'], enc['x']
        return plot

    def hist(self, x=None, y=None, by=None, bins=10, stacked=False, alpha=None,
             var_name='variable', value_name='value',
             interactive=True, width=450, height=300, **kwds):
        _warn_if_unused_keywords('hist', kwds)
        if by is not None:
            raise NotImplementedError('vgplot.hist `by` keyword')
        if x is not None or y is not None:
            raise NotImplementedError('"x" and "y" args to hist()')
        df = self._data.melt(var_name=var_name, value_name=value_name)

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

        spec = _finalize_spec(spec, interactive=interactive,
                              width=width, height=height)
        return VegaLiteAxes(spec, data=df)

    def hexbin(self, x, y, C=None, reduce_C_function=None,
               gridsize=100, alpha=None,
               interactive=True, width=450, height=300, **kwds):
        # TODO: Use actual hexbins rather than a grid heatmap
        _warn_if_unused_keywords('hexbin', kwds)

        if reduce_C_function is not None:
            raise NotImplementedError("Custom reduce_C_function in hexbin")
        if C is None:
            df = self._data[[x, y]]
        else:
            df = self._data[[x, y, C]]

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

        spec = _finalize_spec(spec, interactive=interactive,
                              width=width, height=height)
        return VegaLiteAxes(spec, data=df)

    def kde(self, y=None, bw_method=None, alpha=None,
            interactive=True, width=450, height=300, **kwds):
        from scipy.stats import gaussian_kde as kde

        if y is not None:
            df = self._data[y].to_frame()
        else:
            df = self._data

        tmin, tmax = df.min().min(), df.max().max()
        trange = tmax - tmin
        t = np.linspace(tmin - 0.5 * trange, tmax + 0.5 * trange, 1000)

        kde_df = pd.DataFrame({col: kde(df[col], bw_method=bw_method).evaluate(t)
                               for col in df}, index=t)
        kde_df.index.name = ' '

        f = FramePlotMethods(kde_df)
        return f.line(value_name='Density', alpha=alpha,
                      interactive=interactive,
                      width=width, height=height, **kwds)

    density = kde
