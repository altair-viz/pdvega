import pytest

import pandas as pd
import numpy as np

from pdvega._utils import infer_vegalite_type, unpivot_frame, validate_aggregation

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


def test_unpivot():
    frame = pd.DataFrame({'x': range(10), 'y': range(10), 'z': range(10)})
    df = unpivot_frame(frame, var_name='foo', value_name='bar')
    assert list(df.columns) == ['index', 'foo', 'bar']
    assert set(pd.unique(df['foo'])) == {'x', 'y', 'z'}

    df = unpivot_frame(frame, x='x')
    assert list(df.columns) == ['x', 'variable', 'value']
    assert set(pd.unique(df['variable'])) == {'y', 'z'}

    df = unpivot_frame(frame, y='y')
    assert list(df.columns) == ['index', 'variable', 'value']
    assert set(pd.unique(df['variable'])) == {'y'}

    df = unpivot_frame(frame, y=('y', 'z'))
    assert list(df.columns) == ['index', 'variable', 'value']
    assert set(pd.unique(df['variable'])) == {'y', 'z'}

    df = unpivot_frame(frame, x=('x', 'y'), y='z')
    assert list(df.columns) == ['x', 'y', 'variable', 'value']
    assert set(pd.unique(df['variable'])) == {'z'}


def test_unpivot_bad_cols():
    frame = pd.DataFrame({'x': range(10), 'y': range(10)})

    with pytest.raises(KeyError):
        unpivot_frame(frame, x='foo')

    with pytest.raises(KeyError):
        unpivot_frame(frame, y='foo')

    with pytest.raises(KeyError):
        unpivot_frame(frame, x=('x', 'foo'))

    with pytest.raises(KeyError):
        unpivot_frame(frame, y=('y', 'foo'))


def test_validate_aggregation():
    string_cases = ['max', 'min', 'mean', 'median', 'count', 'sum']
    func_cases = {np.min: 'min', min: 'min',
                  np.max: 'max', max: 'max',
                  np.sum: 'sum', sum: 'sum',
                  np.median: 'median', np.mean: 'mean'}

    for case in string_cases:
        assert validate_aggregation(case) == case

    for case, result in func_cases.items():
        assert validate_aggregation(case) == result

    assert validate_aggregation(None) is None

    with pytest.raises(ValueError) as err:
        validate_aggregation('blah')
    assert str(err.value).startswith("Unrecognized Vega-Lite aggregation")

    with pytest.raises(ValueError) as err:
        validate_aggregation(np.array)
    assert str(err.value).startswith("Unrecognized Vega-Lite aggregation")
