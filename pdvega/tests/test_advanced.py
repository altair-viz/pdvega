import pdvega
import pandas as pd


def test_advanced():
    df = pd.Series(range(10))
    plot = df.vgplot.line()

    plot.spec['encoding']['x']['scale'] = {'zero': False}
    assert 'scale' in plot.spec['encoding']['x']
    assert plot.spec['encoding']['x']['scale']['zero'] is False
