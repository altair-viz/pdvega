"""Common tests for all plotting routines"""
import pytest

import pandas as pd
import pdvega

from .utils import validate_vegalite


@pytest.fixture
def data():
    """A dataframe with quantitative and nominal columns"""
    return pd.DataFrame({
        'x': range(10),
        'y': range(10),
        'z': range(10),
        'a': list('ABCABCABCA'),
        'b': list('ABCABCABCA')
    })


other_chart = pd.Series(range(10)).vgplot(kind='line')
AXES = [
    (None, pdvega.alt.Chart),
    (other_chart, pdvega.alt.LayerChart),
    (pdvega.alt.layer(other_chart), pdvega.alt.LayerChart)
]

FRAME_TEST_CASES = {
    'line': {
        'usecols': ['x', 'y', 'z'],
    },
    'bar': {
        'usecols': ['x', 'y', 'z'],
    },
    'barh': {
        'usecols': ['x', 'y', 'z'],
    },
    'area': {
        'usecols': ['x', 'y', 'z'],
    },
    'scatter': {
        'usecols': ['x', 'y', 'a', 'b'],
        'kwds': {'x': 'x', 'y': 'y', 'c': 'a', 's': 'b'}
    },
    'hist': {
        'usecols': ['x', 'y', 'z'],
    },
    'hexbin': {
        'usecols': ['x', 'y', 'z'],
        'kwds': {'x': 'x', 'y': 'y'}
    },
    'kde': {
        'usecols': ['x', 'y', 'z'],
    },
    'density': {
        'usecols': ['x', 'y', 'z'],
    }
}

SERIES_TEST_CASES = {
    'line': {
        'col': 'x'
    },
    'bar': {
        'col': 'x'
    },
    'barh': {
        'col': 'x'
    },
    'area': {
        'col': 'x'
    },
    'hist': {
        'col': 'x'
    },
    'kde': {
        'col': 'x'
    },
    'density': {
        'col': 'x'
    }
}


def is_stackable(kind):
    return kind in {'bar', 'barh', 'area', 'hist'}


@pytest.mark.parametrize('kind,info', SERIES_TEST_CASES.items())
def test_series_plot_interactive(data, kind, info):
    col = info['col']
    kwds = info.get('kwds', {})
    data = data[col]

    spec = data.vgplot(kind=kind, **kwds)
    validate_vegalite(spec)
    assert 'selection' not in spec.to_dict()

    spec = data.vgplot(kind=kind, **kwds).interactive()
    validate_vegalite(spec)
    s = spec.to_dict()
    assert next(iter(s['selection'].values())) == {'bind': 'scales', 'encodings': ['x', 'y'], 'type': 'interval'}


@pytest.mark.parametrize('kind,info', FRAME_TEST_CASES.items())
def test_frame_plot_interactive(data, kind, info):
    cols = info['usecols']
    kwds = info.get('kwds', {})
    data = data[cols]

    chart = data.vgplot(kind=kind, **kwds)
    validate_vegalite(chart)
    assert 'selection' not in chart.to_dict()

    chart = data.vgplot(kind=kind, **kwds).interactive()
    validate_vegalite(chart)
    s = chart.to_dict()
    assert next(iter(s['selection'].values())) == {'bind': 'scales', 'encodings': ['x', 'y'], 'type': 'interval'}


@pytest.mark.parametrize('kind,info', SERIES_TEST_CASES.items())
def test_series_plot_alpha(data, kind, info):
    col = info['col']
    kwds = info.get('kwds', {})
    data = data[col]

    chart = data.vgplot(kind=kind, alpha=0.5, **kwds)
    validate_vegalite(chart)
    encoding = chart['encoding'].to_dict()
    assert 'opacity' in encoding, encoding.keys()
    assert encoding['opacity']['value'] == 0.5

    chart = data.vgplot(kind=kind, **kwds)
    validate_vegalite(chart)
    assert 'opacity' not in chart['encoding'].to_dict()


@pytest.mark.parametrize('kind,info', SERIES_TEST_CASES.items())
@pytest.mark.parametrize('ax', AXES)
def test_series_plot_ax(data, kind, info, ax):
    col = info['col']
    kwds = info.get('kwds', {})
    data = data[col]

    chart = data.vgplot(kind=kind, ax=ax[0], **kwds)
    validate_vegalite(chart)
    assert isinstance(chart, ax[1])


@pytest.mark.parametrize('kind,info', FRAME_TEST_CASES.items())
def test_frame_plot_alpha(data, kind, info):
    cols = info['usecols']
    kwds = info.get('kwds', {})
    data = data[cols]

    # if alpha is explicitly specified, then opacity should be in the spec
    chart = data.vgplot(kind=kind, alpha=0.5, **kwds)
    validate_vegalite(chart)
    assert chart['encoding'].to_dict()['opacity']['value'] == 0.5

    if is_stackable(kind):
        # stackable plots have a default opacity when not stacked
        chart = data.vgplot(kind=kind, stacked=False, **kwds)
        validate_vegalite(chart)
        assert chart['encoding'].to_dict()['opacity']['value'] == 0.7

        # if only one column is being plotted, then should have no opacity
        chart = data[cols[:1]].vgplot(kind=kind, stacked=False, **kwds)
        validate_vegalite(chart)
        assert 'opacity' not in chart['encoding'].to_dict()

        # if stacked, then should have no opacity
        chart = data.vgplot(kind=kind, stacked=True, **kwds)
        validate_vegalite(chart)
        assert 'opacity' not in chart['encoding'].to_dict()
    else:
        # non-stackable plots have no default opacity
        chart = data.vgplot(kind=kind, **kwds)
        validate_vegalite(chart)
        assert 'opacity' not in chart['encoding'].to_dict()


@pytest.mark.parametrize('kind,info', FRAME_TEST_CASES.items())
@pytest.mark.parametrize('ax', AXES)
def test_frame_plot_ax(data, kind, info, ax):
    cols = info['usecols']
    kwds = info.get('kwds', {})
    data = data[cols]

    chart = data.vgplot(kind=kind, ax=ax[0], **kwds)
    validate_vegalite(chart)
    assert isinstance(chart, ax[1])


@pytest.mark.parametrize('kind,info', SERIES_TEST_CASES.items())
def test_series_plot_width_height(data, kind, info):
    col = info['col']
    kwds = info.get('kwds', {})
    data = data[col]

    spec = data.vgplot(kind=kind, width=300, height=200, **kwds)
    validate_vegalite(spec)
    assert (spec['width'], spec['height']) == (300, 200)

    spec = data.vgplot(kind=kind, **kwds)
    validate_vegalite(spec)
    s = spec.to_dict()
    assert (s['width'], s['height']) == (450, 300)


@pytest.mark.parametrize('kind,info', FRAME_TEST_CASES.items())
def test_frame_plot_width_height(data, kind, info):
    cols = info['usecols']
    kwds = info.get('kwds', {})
    data = data[cols]

    spec = data.vgplot(kind=kind, width=300, height=200, **kwds)
    validate_vegalite(spec)
    s = spec.to_dict()
    assert (s['width'], s['height']) == (300, 200)

    spec = data.vgplot(kind=kind, **kwds)
    validate_vegalite(spec)
    s = spec.to_dict()
    assert (s['width'], s['height']) == (450, 300)


@pytest.mark.parametrize('kind,info', SERIES_TEST_CASES.items())
def test_series_plot_kwd_warnings(data, kind, info):
    col = info['col']
    kwds = info.get('kwds', {})
    data = data[col]

    with pytest.warns(UserWarning, match="Unrecognized keywords in vgplot.[a-z]+\(\): 'unrecognized_arg'"):
        data.vgplot(kind=kind, unrecognized_arg=None, **kwds)

    with pytest.warns(UserWarning):
        data.vgplot(kind=kind, unrecognized1=None, unrecognized2=None, **kwds)


@pytest.mark.parametrize('kind,info', FRAME_TEST_CASES.items())
def test_frame_plot_kwd_warnings(data, kind, info):
    cols = info['usecols']
    kwds = info.get('kwds', {})
    data = data[cols]

    with pytest.warns(UserWarning, match="Unrecognized keywords in vgplot.[a-z]+\(\): 'unrecognized_arg'"):
        data.vgplot(kind=kind, unrecognized_arg=None, **kwds)

    with pytest.warns(UserWarning):
        data.vgplot(kind=kind, unrecognized1=None, unrecognized2=None, **kwds)
