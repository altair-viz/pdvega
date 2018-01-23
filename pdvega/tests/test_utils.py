import pytest

import pandas as pd
import numpy as np

from pdvega._utils import infer_vegalite_type

test_cases = [
    (pd.Series(np.random.rand(20)), 'quantitative'),
    (pd.Series(range(4)), 'ordinal'),
    (pd.Series(range(40)), 'quantitative'),
    (pd.Series(['A', 'B', 'C', 'D']), 'nominal'),
    (pd.Categorical(['a', 'b', 'c']), 'nominal'),
    (pd.date_range('2017', freq='D', periods=10), 'temporal'),
    (pd.timedelta_range(0, periods=7), 'temporal')
]


@pytest.mark.parametrize('data,type', test_cases)
def test_infer_vegalite_type(data, type):
    assert infer_vegalite_type(data) == type
