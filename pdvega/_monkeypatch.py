from pandas import DataFrame, Series
try:
    # new location
    from pandas.core.accessor import AccessorProperty
except ImportError:
    # old location
    from pandas.core.base import AccessorProperty
from ._plotting import FrameVgPlotMethods, SeriesVgPlotMethods


def monkeypatch_pandas():
    DataFrame.vgplot = AccessorProperty(FrameVgPlotMethods, FrameVgPlotMethods)
    Series.vgplot = AccessorProperty(SeriesVgPlotMethods, SeriesVgPlotMethods)
