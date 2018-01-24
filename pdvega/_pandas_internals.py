from pandas.plotting._core import FramePlotMethods, SeriesPlotMethods

try:
    from pandas.api.extensions import (register_dataframe_accessor,
                                       register_series_accessor)
except ImportError:
    from pandas.core.accessor import AccessorProperty
except ImportError:  # Pandas before 0.22.0
    from pandas.core.base import AccessorProperty

try:
    from pandas.api.types import infer_dtype as infer_dtype
except ImportError:  # Pandas before 0.20.0
    from pandas.lib import infer_dtype as infer_dtype
