import pdvega
import pandas as pd


IGNORE = object()


def _check_encodings(spec, **fields):
    assert set(spec['encoding'].keys()) == set(fields.keys())
    for encoding, expected_field in fields.items():
        if expected_field is IGNORE:
            continue
        actual_field = spec['encoding'][encoding]['field']
        if actual_field != expected_field:
            raise ValueError("Expected '{0}' encoding to be '{1}'; got '{2}'"
                             "".format(encoding, expected_field, actual_field))


def _get_data(spec):
    return pd.DataFrame.from_records(spec['data']['values'])


def test_line_plot_simple():
    df = pd.DataFrame({'x': [1,4,2,3,5],
                       'y': [6,3,4,5,2]})

    plot = df.vgplot.line()
    assert plot.spec['mark'] == 'line'
    _check_encodings(plot.spec, x='index', y='value', color='variable')
    data = _get_data(plot.spec)
    assert set(pd.unique(data['variable'])) == {'x', 'y'}


def test_line_plot_xy():
    df = pd.DataFrame({'x': [1,4,2,3,5],
                       'y': [6,3,4,5,2],
                       'z': range(5)})

    plot = df.vgplot.line(x='x', y='y')
    assert plot.spec['mark'] == 'line'
    _check_encodings(plot.spec, x='x', y='value', color='variable')
    data = _get_data(plot.spec)
    assert set(pd.unique(data['variable'])) == {'y'}


def test_scatter_plot_simple():
    df = pd.DataFrame({'x': [1,4,2,3,5],
                       'y': [6,3,4,5,2]})

    plot = df.vgplot.scatter(x='x', y='y')
    assert plot.spec['mark'] == 'circle'
    _check_encodings(plot.spec, x='x', y='y')


def test_scatter_plot_color_size():
    df = pd.DataFrame({'x': [1,4,2,3,5],
                       'y': [6,3,4,5,2],
                       'c': range(5),
                       's': range(5)})

    plot = df.vgplot.scatter(x='x', y='y', c='c', s='s')
    assert plot.spec['mark'] == 'circle'
    _check_encodings(plot.spec, x='x', y='y', color='c', size='s')


def test_bar_plot_simple():
    df = pd.DataFrame({'x': [1,4,2,3,5],
                       'y': [6,3,4,5,2]})

    plot = df.vgplot.bar()
    assert plot.spec['mark'] == 'bar'
    _check_encodings(plot.spec, x='index', y='value',
                     color='variable', opacity=IGNORE)
    data = _get_data(plot.spec)
    assert set(pd.unique(data['variable'])) == {'x', 'y'}


def test_bar_plot_xy():
    df = pd.DataFrame({'x': [1,4,2,3,5],
                       'y': [6,3,4,5,2]})

    plot = df.vgplot.bar(x='x', y='y')
    assert plot.spec['mark'] == 'bar'
    _check_encodings(plot.spec, x='x', y='value',
                     color='variable', opacity=IGNORE)
    data = _get_data(plot.spec)
    assert set(pd.unique(data['variable'])) == {'y'}
