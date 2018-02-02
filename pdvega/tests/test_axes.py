import pytest
import pandas as pd

import pdvega


def test_max_rows():
    df = pd.Series(range(20))
    plot = df.vgplot.line()
    plot.max_rows = 10

    with pytest.raises(pdvega.MaxRowsExceeded) as err:
        plot._ipython_display_()
    assert '20' in str(err.value)
    assert '10' in str(err.value)
