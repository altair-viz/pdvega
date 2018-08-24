import pdvega # flake8: noqa
import pandas as pd


def test_advanced():
    df = pd.Series(range(10))
    plot = df.vgplot.line()

    plot['encoding']['x']['scale'] = {'zero': False}
    spec = plot.to_dict()
    assert 'scale' in spec['encoding']['x']
    assert spec['encoding']['x']['scale']['zero'] is False
