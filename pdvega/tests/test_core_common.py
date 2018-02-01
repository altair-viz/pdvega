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


COMMON_ARGS = {
    'alpha': [None, 0.5],
    'interactive': [True, False],
    'width': [300, 450],
    'height': [200, 300],
}

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
    return kind in ['bar', 'barh', 'area', 'hist']


@pytest.mark.parametrize('kind,info', SERIES_TEST_CASES.items())
def test_series_plot_interactive(data, kind, info):
    col = info['col']
    kwds = info.get('kwds', {})
    data = data[col]

    spec = data.vgplot(kind=kind, **kwds).spec
    validate_vegalite(spec)
    assert spec['selection']['grid'] == {"type": "interval", "bind": "scales"}

    spec = data.vgplot(kind=kind, interactive=True, **kwds).spec
    validate_vegalite(spec)
    assert spec['selection']['grid'] == {"type": "interval", "bind": "scales"}

    spec = data.vgplot(kind=kind, interactive=False, **kwds).spec
    validate_vegalite(spec)
    assert 'selection' not in spec


@pytest.mark.parametrize('kind,info', FRAME_TEST_CASES.items())
def test_frame_plot_interactive(data, kind, info):
    cols = info['usecols']
    kwds = info.get('kwds', {})
    data = data[cols]

    spec = data.vgplot(kind=kind, **kwds).spec
    validate_vegalite(spec)
    assert spec['selection']['grid'] == {"type": "interval", "bind": "scales"}

    spec = data.vgplot(kind=kind, interactive=True, **kwds).spec
    validate_vegalite(spec)
    assert spec['selection']['grid'] == {"type": "interval", "bind": "scales"}

    spec = data.vgplot(kind=kind, interactive=False, **kwds).spec
    validate_vegalite(spec)
    assert 'selection' not in spec


@pytest.mark.parametrize('kind,info', SERIES_TEST_CASES.items())
def test_series_plot_alpha(data, kind, info):
    col = info['col']
    kwds = info.get('kwds', {})
    data = data[col]

    spec = data.vgplot(kind=kind, alpha=0.5, **kwds).spec
    validate_vegalite(spec)
    assert spec['encoding']['opacity']['value'] == 0.5

    spec = data.vgplot(kind=kind, **kwds).spec
    validate_vegalite(spec)
    assert 'opacity' not in spec['encoding']


@pytest.mark.parametrize('kind,info', FRAME_TEST_CASES.items())
def test_frame_plot_alpha(data, kind, info):
    cols = info['usecols']
    kwds = info.get('kwds', {})
    data = data[cols]

    # if alpha is explicitly specified, then opacity should be in the spec
    spec = data.vgplot(kind=kind, alpha=0.5, **kwds).spec
    validate_vegalite(spec)
    assert spec['encoding']['opacity']['value'] == 0.5

    if is_stackable(kind):
        # stackable plots have a default opacity when not stacked
        spec = data.vgplot(kind=kind, stacked=False, **kwds).spec
        validate_vegalite(spec)
        assert spec['encoding']['opacity']['value'] == 0.7

        # if only one column is being plotted, then should have no opacity
        spec = data[cols[:1]].vgplot(kind=kind, stacked=False, **kwds).spec
        validate_vegalite(spec)
        assert 'opacity' not in spec['encoding']

        # if stacked, then should have no opacity
        spec = data.vgplot(kind=kind, stacked=True, **kwds).spec
        validate_vegalite(spec)
        assert 'opacity' not in spec['encoding']
    else:
        # non-stackable plots have no default opacity
        spec = data.vgplot(kind=kind, **kwds).spec
        validate_vegalite(spec)
        assert 'opacity' not in spec['encoding']


@pytest.mark.parametrize('kind,info', SERIES_TEST_CASES.items())
def test_series_plot_width_height(data, kind, info):
    col = info['col']
    kwds = info.get('kwds', {})
    data = data[col]

    spec = data.vgplot(kind=kind, width=300, height=200, **kwds).spec
    validate_vegalite(spec)
    assert (spec['width'], spec['height']) == (300, 200)

    spec = data.vgplot(kind=kind, **kwds).spec
    validate_vegalite(spec)
    assert (spec['width'], spec['height']) == (450, 300)


@pytest.mark.parametrize('kind,info', FRAME_TEST_CASES.items())
def test_frame_plot_width_height(data, kind, info):
    cols = info['usecols']
    kwds = info.get('kwds', {})
    data = data[cols]

    spec = data.vgplot(kind=kind, width=300, height=200, **kwds).spec
    validate_vegalite(spec)
    assert (spec['width'], spec['height']) == (300, 200)

    spec = data.vgplot(kind=kind, **kwds).spec
    validate_vegalite(spec)
    assert (spec['width'], spec['height']) == (450, 300)


@pytest.mark.parametrize('kind,info', SERIES_TEST_CASES.items())
def test_series_plot_kwd_warnings(data, kind, info):
    col = info['col']
    kwds = info.get('kwds', {})
    data = data[col]

    with pytest.warns(UserWarning, match="Unrecognized keywords in vgplot.[a-z]+\(\): 'unrecognized_arg'"):
        plot = data.vgplot(kind=kind, unrecognized_arg=None, **kwds)

    with pytest.warns(UserWarning):
        plot = data.vgplot(kind=kind, unrecognized1=None, unrecognized2=None, **kwds)


@pytest.mark.parametrize('kind,info', FRAME_TEST_CASES.items())
def test_frame_plot_kwd_warnings(data, kind, info):
    cols = info['usecols']
    kwds = info.get('kwds', {})
    data = data[cols]

    with pytest.warns(UserWarning, match="Unrecognized keywords in vgplot.[a-z]+\(\): 'unrecognized_arg'"):
        plot = data.vgplot(kind=kind, unrecognized_arg=None, **kwds)

    with pytest.warns(UserWarning):
        plot = data.vgplot(kind=kind, unrecognized1=None, unrecognized2=None, **kwds)
