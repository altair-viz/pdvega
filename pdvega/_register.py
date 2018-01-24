from ._pandas_internals import (register_dataframe_accessor,
                                register_series_accessor)

from ._plotting import FrameVgPlotMethods, SeriesVgPlotMethods


def register():
    register_dataframe_accessor('vgplot')(FrameVgPlotMethods)
    register_series_accessor('vgplot')(SeriesVgPlotMethods)
