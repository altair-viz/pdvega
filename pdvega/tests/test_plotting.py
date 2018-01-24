import pdvega
import pandas as pd

import jsonschema

from ..schema import VEGALITE_SCHEMA


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


def validate_vegalite(spec):
    return jsonschema.validate(spec, VEGALITE_SCHEMA)


def test_line_simple():
    df = pd.DataFrame({'x': [1,4,2,3,5],
                       'y': [6,3,4,5,2]})

    plot = df.vgplot.line()
    validate_vegalite(plot.spec)
    assert plot.spec['mark'] == 'line'
    _check_encodings(plot.spec, x='index', y='value', color='variable')
    data = _get_data(plot.spec)
    assert set(pd.unique(data['variable'])) == {'x', 'y'}


def test_line_xy():
    df = pd.DataFrame({'x': [1,4,2,3,5],
                       'y': [6,3,4,5,2],
                       'z': range(5)})

    plot = df.vgplot.line(x='x', y='y')
    validate_vegalite(plot.spec)
    assert plot.spec['mark'] == 'line'
    _check_encodings(plot.spec, x='x', y='value', color='variable')
    data = _get_data(plot.spec)
    assert set(pd.unique(data['variable'])) == {'y'}


def test_series_line():
    ser = pd.Series([3, 2, 3, 2, 3])
    plot = ser.vgplot.line()
    validate_vegalite(plot.spec)
    assert plot.spec['mark'] == 'line'
    _check_encodings(plot.spec, x='index', y='0')


def test_scatter_simple():
    df = pd.DataFrame({'x': [1,4,2,3,5],
                       'y': [6,3,4,5,2]})

    plot = df.vgplot.scatter(x='x', y='y')
    validate_vegalite(plot.spec)
    assert plot.spec['mark'] == 'circle'
    _check_encodings(plot.spec, x='x', y='y')


def test_scatter_color_size():
    df = pd.DataFrame({'x': [1,4,2,3,5],
                       'y': [6,3,4,5,2],
                       'c': range(5),
                       's': range(5)})

    plot = df.vgplot.scatter(x='x', y='y', c='c', s='s')
    validate_vegalite(plot.spec)
    assert plot.spec['mark'] == 'circle'
    _check_encodings(plot.spec, x='x', y='y', color='c', size='s')


def test_bar_simple():
    df = pd.DataFrame({'x': [1,4,2,3,5],
                       'y': [6,3,4,5,2]})

    plot = df.vgplot.bar()
    validate_vegalite(plot.spec)
    assert plot.spec['mark'] == 'bar'
    _check_encodings(plot.spec, x='index', y='value',
                     color='variable', opacity=IGNORE)
    data = _get_data(plot.spec)
    assert set(pd.unique(data['variable'])) == {'x', 'y'}
    assert plot.spec['encoding']['y']['stack'] is None


def test_bar_stacked():
    df = pd.DataFrame({'x': [1,4,2,3,5],
                       'y': [6,3,4,5,2]})

    plot = df.vgplot.bar(stacked=True)
    validate_vegalite(plot.spec)
    assert plot.spec['mark'] == 'bar'
    _check_encodings(plot.spec, x='index', y='value', color='variable')
    data = _get_data(plot.spec)
    assert set(pd.unique(data['variable'])) == {'x', 'y'}
    assert plot.spec['encoding']['y']['stack'] == "zero"


def test_bar_xy():
    df = pd.DataFrame({'x': [1,4,2,3,5],
                       'y': [6,3,4,5,2]})

    plot = df.vgplot.bar(x='x', y='y')
    validate_vegalite(plot.spec)
    assert plot.spec['mark'] == 'bar'
    _check_encodings(plot.spec, x='x', y='value',
                     color='variable', opacity=IGNORE)
    data = _get_data(plot.spec)
    assert set(pd.unique(data['variable'])) == {'y'}
    assert plot.spec['encoding']['y']['stack'] is None


def test_bar_xy_stacked():
    df = pd.DataFrame({'x': [1,4,2,3,5],
                       'y': [6,3,4,5,2]})

    plot = df.vgplot.bar(x='x', y='y', stacked=True)
    validate_vegalite(plot.spec)
    assert plot.spec['mark'] == 'bar'
    _check_encodings(plot.spec, x='x', y='value', color='variable')
    data = _get_data(plot.spec)
    assert set(pd.unique(data['variable'])) == {'y'}
    assert plot.spec['encoding']['y']['stack'] == "zero"


def test_series_bar():
    ser = pd.Series([4,5,4,5], index=['A', 'B', 'C', 'D'])
    plot = ser.vgplot.bar()
    validate_vegalite(plot.spec)
    assert plot.spec['mark'] == 'bar'
    _check_encodings(plot.spec, x='index', y='0')


def test_barh_simple():
    df = pd.DataFrame({'x': [1,4,2,3,5],
                       'y': [6,3,4,5,2]})

    plot = df.vgplot.barh()
    validate_vegalite(plot.spec)
    assert plot.spec['mark'] == 'bar'
    _check_encodings(plot.spec, y='index', x='value',
                     color='variable', opacity=IGNORE)
    data = _get_data(plot.spec)
    assert set(pd.unique(data['variable'])) == {'x', 'y'}
    assert plot.spec['encoding']['x']['stack'] is None


def test_barh_stacked():
    df = pd.DataFrame({'x': [1,4,2,3,5],
                       'y': [6,3,4,5,2]})

    plot = df.vgplot.barh(stacked=True)
    validate_vegalite(plot.spec)
    assert plot.spec['mark'] == 'bar'
    _check_encodings(plot.spec, y='index', x='value', color='variable')
    data = _get_data(plot.spec)
    assert set(pd.unique(data['variable'])) == {'x', 'y'}
    assert plot.spec['encoding']['x']['stack'] == "zero"


def test_barh_xy():
    df = pd.DataFrame({'x': [1,4,2,3,5],
                       'y': [6,3,4,5,2]})

    plot = df.vgplot.barh(x='x', y='y')
    validate_vegalite(plot.spec)
    assert plot.spec['mark'] == 'bar'
    _check_encodings(plot.spec, x='value', y='x',
                     color='variable', opacity=IGNORE)
    data = _get_data(plot.spec)
    assert set(pd.unique(data['variable'])) == {'y'}
    assert plot.spec['encoding']['x']['stack'] is None


def test_barh_xy_stacked():
    df = pd.DataFrame({'x': [1,4,2,3,5],
                       'y': [6,3,4,5,2]})

    plot = df.vgplot.barh(x='x', y='y', stacked=True)
    validate_vegalite(plot.spec)
    assert plot.spec['mark'] == 'bar'
    _check_encodings(plot.spec, x='value', y='x', color='variable')
    data = _get_data(plot.spec)
    assert set(pd.unique(data['variable'])) == {'y'}
    assert plot.spec['encoding']['x']['stack'] == "zero"


def test_series_barh():
    ser = pd.Series([4,5,4,5], index=['A', 'B', 'C', 'D'])
    plot = ser.vgplot.barh()
    validate_vegalite(plot.spec)
    assert plot.spec['mark'] == 'bar'
    _check_encodings(plot.spec, y='index', x='0')


def test_df_area_simple():
    df = pd.DataFrame({'x': [1,4,2,3,5],
                       'y': [6,3,4,5,2]})

    plot = df.vgplot.area()
    validate_vegalite(plot.spec)
    assert plot.spec['mark'] == 'area'
    _check_encodings(plot.spec, x='index', y='value', color='variable')
    data = _get_data(plot.spec)
    assert set(pd.unique(data['variable'])) == {'x', 'y'}
    assert plot.spec['encoding']['y']['stack'] == 'zero'


def test_df_area_unstacked():
    df = pd.DataFrame({'x': [1,4,2,3,5],
                       'y': [6,3,4,5,2]})

    plot = df.vgplot.area(stacked=False)
    validate_vegalite(plot.spec)
    assert plot.spec['mark'] == 'area'
    _check_encodings(plot.spec, x='index', y='value', color='variable', opacity=IGNORE)
    data = _get_data(plot.spec)
    assert set(pd.unique(data['variable'])) == {'x', 'y'}
    assert plot.spec['encoding']['y']['stack'] is None
    assert plot.spec['encoding']['opacity']['value'] == 0.7


def test_df_area_xy():
    df = pd.DataFrame({'x': [1,4,2,3,5],
                       'y': [6,3,4,5,2],
                       'z': range(5)})

    plot = df.vgplot.area(x='x', y='y')
    validate_vegalite(plot.spec)
    assert plot.spec['mark'] == 'area'
    _check_encodings(plot.spec, x='x', y='value', color='variable')
    data = _get_data(plot.spec)
    assert set(pd.unique(data['variable'])) == {'y'}
    assert plot.spec['encoding']['y']['stack'] == 'zero'


def test_df_area_xy_unstacked():
    df = pd.DataFrame({'x': [1,4,2,3,5],
                       'y': [6,3,4,5,2],
                       'z': range(5)})

    plot = df.vgplot.area(x='x', y='y', stacked=False)
    validate_vegalite(plot.spec)
    assert plot.spec['mark'] == 'area'
    _check_encodings(plot.spec, x='x', y='value', color='variable', opacity=IGNORE)
    data = _get_data(plot.spec)
    assert set(pd.unique(data['variable'])) == {'y'}
    assert plot.spec['encoding']['y']['stack'] is None
    assert plot.spec['encoding']['opacity']['value'] == 0.7


def test_series_area():
    ser = pd.Series([3, 2, 3, 2, 3])
    plot = ser.vgplot.area()
    validate_vegalite(plot.spec)
    assert plot.spec['mark'] == 'area'
    _check_encodings(plot.spec, x='index', y='0')


def test_df_hist():
    df = pd.DataFrame({'x': range(10),
                       'y': range(10)})
    plot = df.vgplot.hist(bins=5)
    assert plot.spec['mark'] == 'bar'
    _check_encodings(plot.spec, x='value', y=IGNORE, color='variable')
    assert plot.spec['encoding']['x']['bin'] == {'maxbins': 5}
    assert plot.spec['encoding']['y']['aggregate'] == 'count'
    assert plot.spec['encoding']['y']['stack'] == None


def test_df_hist_stacked():
    df = pd.DataFrame({'x': range(10),
                       'y': range(10)})
    plot = df.vgplot.hist(bins=5, stacked=True)
    assert plot.spec['mark'] == 'bar'
    _check_encodings(plot.spec, x='value', y=IGNORE, color='variable')
    assert plot.spec['encoding']['x']['bin'] == {'maxbins': 5}
    assert plot.spec['encoding']['y']['aggregate'] == 'count'
    assert plot.spec['encoding']['y']['stack'] == 'zero'


def test_series_hist():
    ser = pd.Series(range(10))
    plot = ser.vgplot.hist(bins=5)
    assert plot.spec['mark'] == 'bar'
    _check_encodings(plot.spec, x='0', y=IGNORE)
    assert plot.spec['encoding']['x']['bin'] == {'maxbins': 5}
    assert plot.spec['encoding']['y']['aggregate'] == 'count'


def test_df_hexbin():
    df = pd.DataFrame({'x': range(10),
                       'y': range(10),
                       'C': range(10)})
    gridsize=10
    plot = df.vgplot.hexbin(x='x', y='y', gridsize=gridsize)
    assert plot.spec['mark'] == 'rect'
    _check_encodings(plot.spec, x='x', y='y', color=IGNORE)
    assert plot.spec['encoding']['x']['bin'] == {"maxbins": gridsize}
    assert plot.spec['encoding']['y']['bin'] == {"maxbins": gridsize}
    assert plot.spec['encoding']['color']['aggregate'] == "count"


def test_df_hexbin_C():
    df = pd.DataFrame({'x': range(10),
                       'y': range(10),
                       'C': range(10)})
    gridsize=10
    plot = df.vgplot.hexbin(x='x', y='y', C='C', gridsize=gridsize)
    assert plot.spec['mark'] == 'rect'
    _check_encodings(plot.spec, x='x', y='y', color='C')
    assert plot.spec['encoding']['x']['bin'] == {"maxbins": gridsize}
    assert plot.spec['encoding']['y']['bin'] == {"maxbins": gridsize}
    assert plot.spec['encoding']['color']['aggregate'] == "mean"
