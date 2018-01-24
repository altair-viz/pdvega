from pandas import DataFrame, Series
from ._pandas_internals import AccessorProperty
from ._plotting import FrameVgPlotMethods, SeriesVgPlotMethods


def monkeypatch_pandas():
    DataFrame.vgplot = AccessorProperty(FrameVgPlotMethods, FrameVgPlotMethods)
    Series.vgplot = AccessorProperty(SeriesVgPlotMethods, SeriesVgPlotMethods)
