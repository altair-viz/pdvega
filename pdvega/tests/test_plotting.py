import pytest

import numpy as np
import pandas as pd

import pdvega
from pdvega.tests import utils


def test_scatter_matrix():
    df = pd.DataFrame({'x': range(5),
                       'y': range(5),
                       'label': list('ABABA')})
    # no color or size specified
    plot = pdvega.scatter_matrix(df)
    utils.validate_vegalite(plot)
    spec = plot.to_dict()
    assert spec['repeat']['row'] == ['x', 'y']
    assert spec['repeat']['column'] == ['y', 'x']
    assert spec['spec']['encoding']['color']['condition']['value'] == 'steelblue'

    # with color specified
    plot = pdvega.scatter_matrix(df, c='label')
    utils.validate_vegalite(plot)
    spec = plot.to_dict()
    assert spec['repeat']['row'] == ['x', 'y']
    assert spec['repeat']['column'] == ['y', 'x']
    assert spec['spec']['encoding']['color']['condition']['field'] == 'label'

    # with size specified
    plot = pdvega.scatter_matrix(df, s='label')
    utils.validate_vegalite(plot)
    spec = plot.to_dict()
    assert spec['repeat']['row'] == ['x', 'y']
    assert spec['repeat']['column'] == ['y', 'x']
    assert spec['spec']['encoding']['color']['condition']['value'] == 'steelblue'
    assert spec['spec']['encoding']['size']['field'] == 'label'

    # test figsize keyword
    figsize = (8, 6)
    dpi = 40
    ncols = 2
    plot = pdvega.scatter_matrix(df, figsize=figsize, dpi=dpi)
    utils.validate_vegalite(plot)
    spec = plot.to_dict()
    assert np.allclose(spec['spec']['width'],
                       0.8 * dpi * figsize[0] / ncols)
    assert np.allclose(spec['spec']['height'],
                       0.8 * dpi * figsize[1] / ncols)


def test_parallel_coordinates():
    data = pd.DataFrame({'x': range(10),
                         'y': range(10),
                         'z': range(10),
                         'c': list('ABABABABAB')})
    plot = pdvega.parallel_coordinates(data, 'c', alpha=0.5)
    utils.validate_vegalite(plot)
    utils.check_encodings(plot, x='variable', y='value',
                          color='c', detail='index', opacity=utils.IGNORE)

    spec = plot.to_dict()
    enc = spec['encoding']
    assert spec['mark'] == 'line'
    assert enc['x']['type'] == 'nominal'
    assert enc['y']['type'] == 'quantitative'
    assert enc['color']['type'] == 'nominal'
    assert enc['detail']['type'] == 'quantitative'
    assert enc['opacity']['value'] == 0.5

    df = utils.get_data(plot)
    assert set(pd.unique(df['variable'])) == {'x', 'y', 'z'}

    plot = pdvega.parallel_coordinates(data, 'c', cols=['x', 'y'])
    utils.validate_vegalite(plot)
    utils.check_encodings(plot, x='variable', y='value',
                          color='c', detail='index')
    spec = plot.to_dict()
    enc = spec['encoding']
    assert spec['mark'] == 'line'
    assert enc['x']['type'] == 'nominal'
    assert enc['y']['type'] == 'quantitative'
    assert enc['color']['type'] == 'nominal'
    assert enc['detail']['type'] == 'quantitative'
    df = utils.get_data(plot)
    assert set(pd.unique(df['variable'])) == {'x', 'y'}


def test_andrews_curves():
    data = pd.DataFrame({'x': range(10),
                         'y': range(10),
                         'z': range(10),
                         'c': list('ABABABABAB')})
    n_samples = 120
    n_points = len(data)
    plot = pdvega.andrews_curves(data, 'c', samples=120, alpha=0.5)
    utils.validate_vegalite(plot)
    utils.check_encodings(plot, x='t', y=' ',
                          color='c', detail='sample', opacity=utils.IGNORE)

    spec = plot.to_dict()
    enc = spec['encoding']
    assert spec['mark'] == 'line'
    assert enc['x']['type'] == 'quantitative'
    assert enc['y']['type'] == 'quantitative'
    assert enc['color']['type'] == 'nominal'
    assert enc['detail']['type'] == 'quantitative'
    assert enc['opacity']['value'] == 0.5

    df = utils.get_data(plot)
    assert len(df) == n_samples * n_points


@pytest.mark.parametrize('lag', [1, 5])
def test_lag_plot(lag):
    data = pd.DataFrame({'x': range(10),
                         'y': range(10)})

    # test series input
    plot = pdvega.lag_plot(data['x'], lag=lag)
    lag_data = utils.get_data(plot)

    spec = plot.to_dict()
    assert spec['mark'] == 'point'
    assert spec['encoding']['x']['type'] == 'quantitative'
    assert spec['encoding']['y']['type'] == 'quantitative'

    utils.check_encodings(plot, x='y(t)', y='y(t + {0})'.format(lag))
    assert lag_data.shape == (data.shape[0] - lag, 2)

    # test dataframe input
    plot = pdvega.lag_plot(data, lag=lag)
    lag_data = utils.get_data(plot)
    spec = plot.to_dict()

    assert spec['mark'] == 'point'
    assert spec['encoding']['x']['type'] == 'quantitative'
    assert spec['encoding']['y']['type'] == 'quantitative'
    assert spec['encoding']['color']['type'] == 'nominal'
    utils.check_encodings(plot, x='y(t)', y='y(t + {0})'.format(lag),
                          color='variable')
    assert lag_data.shape == (2 * (data.shape[0] - lag), 3)
