import pytest

import pandas as pd

import altair as alt

from pdvega.tests import utils


def test_line_simple():
    df = pd.DataFrame({"x": [1, 4, 2, 3, 5], "y": [6, 3, 4, 5, 2]})

    plot = df.vgplot.line()
    utils.validate_vegalite(plot)

    assert plot.mark == "line"

    utils.check_encodings(plot, x="index", y="value",
                          color="variable")
    data = plot.data
    assert set(pd.unique(data["variable"])) == {"x", "y"}


def test_line_xy():
    df = pd.DataFrame({"x": [1, 4, 2, 3, 5], "y": [6, 3, 4, 5, 2], "z": range(5)})

    plot = df.vgplot.line(x="x", y="y")
    utils.validate_vegalite(plot)
    assert plot.mark == "line"

    utils.check_encodings(plot, x="x", y="value",
                          color="variable", order="index")
    data = plot.data
    assert set(pd.unique(data["variable"])) == {"y"}


def test_series_line():
    ser = pd.Series([3, 2, 3, 2, 3])
    plot = ser.vgplot.line()
    utils.validate_vegalite(plot)
    assert plot.mark == "line"
    utils.check_encodings(plot, x="index", y="0")


def test_scatter_simple():
    df = pd.DataFrame({"x": [1, 4, 2, 3, 5], "y": [6, 3, 4, 5, 2]})

    plot = df.vgplot.scatter(x="x", y="y")
    utils.validate_vegalite(plot)
    assert plot.mark == "point"
    utils.check_encodings(plot, x="x", y="y")


def test_scatter_color_size():
    df = pd.DataFrame(
        {"x": [1, 4, 2, 3, 5], "y": [6, 3, 4, 5, 2], "c": range(5), "s": range(5)}
    )

    plot = df.vgplot.scatter(x="x", y="y", c="c", s="s")
    utils.validate_vegalite(plot)
    assert plot.mark == "point"
    utils.check_encodings(plot, x="x", y="y", color="c", size="s")


def test_scatter_common_columns():
    df = pd.DataFrame({"x": [1, 4, 2, 3, 5], "y": [6, 3, 4, 5, 2]})

    plot = df.vgplot.scatter(x="x", y="y", c="y")
    utils.validate_vegalite(plot)
    assert plot.mark == "point"
    utils.check_encodings(plot, x="x", y="y", color="y")


def test_bar_simple():
    df = pd.DataFrame({"x": [1, 4, 2, 3, 5], "y": [6, 3, 4, 5, 2]})

    plot = df.vgplot.bar()
    utils.validate_vegalite(plot)
    assert plot.mark == "bar"
    utils.check_encodings(
        plot, x="index", y="value", color="variable",
        opacity=utils.IGNORE
    )
    data = plot.data
    assert set(pd.unique(data["variable"])) == {"x", "y"}
    assert plot["encoding"]["y"]["stack"] is None


def test_bar_stacked():
    df = pd.DataFrame({"x": [1, 4, 2, 3, 5], "y": [6, 3, 4, 5, 2]})

    plot = df.vgplot.bar(stacked=True)
    utils.validate_vegalite(plot)
    assert plot.mark == "bar"
    utils.check_encodings(plot, x="index", y="value", color="variable")
    data = plot.data
    assert set(pd.unique(data["variable"])) == {"x", "y"}
    assert plot["encoding"]["y"]["stack"] == "zero"


def test_bar_xy():
    df = pd.DataFrame({"x": [1, 4, 2, 3, 5], "y": [6, 3, 4, 5, 2]})

    plot = df.vgplot.bar(x="x", y="y")
    utils.validate_vegalite(plot)
    assert plot.mark == "bar"
    utils.check_encodings(plot, x="x", y="value", color="variable")
    data = plot.data
    assert set(pd.unique(data["variable"])) == {"y"}
    assert plot["encoding"]["y"]["stack"] is None


def test_bar_xy_stacked():
    df = pd.DataFrame({"x": [1, 4, 2, 3, 5], "y": [6, 3, 4, 5, 2]})

    plot = df.vgplot.bar(x="x", y="y", stacked=True)
    utils.validate_vegalite(plot)
    assert plot.mark == "bar"
    utils.check_encodings(plot, x="x", y="value", color="variable")
    data = plot.data
    assert set(pd.unique(data["variable"])) == {"y"}
    assert plot["encoding"]["y"]["stack"] == "zero"


def test_series_bar():
    ser = pd.Series([4, 5, 4, 5], index=["A", "B", "C", "D"])
    plot = ser.vgplot.bar()
    utils.validate_vegalite(plot)
    assert plot.mark == "bar"
    utils.check_encodings(plot, x="index", y="0")


def test_barh_simple():
    df = pd.DataFrame({"x": [1, 4, 2, 3, 5], "y": [6, 3, 4, 5, 2]})

    plot = df.vgplot.barh()
    utils.validate_vegalite(plot)
    assert plot.mark == "bar"
    utils.check_encodings(
        plot, y="index", x="value", color="variable",
        opacity=utils.IGNORE
    )
    data = plot.data
    assert set(pd.unique(data["variable"])) == {"x", "y"}
    assert plot["encoding"]["x"]["stack"] is None


def test_barh_stacked():
    df = pd.DataFrame({"x": [1, 4, 2, 3, 5], "y": [6, 3, 4, 5, 2]})

    plot = df.vgplot.barh(stacked=True)
    utils.validate_vegalite(plot)
    assert plot.mark == "bar"
    utils.check_encodings(plot, y="index", x="value", color="variable")
    data = plot.data
    assert set(pd.unique(data["variable"])) == {"x", "y"}
    assert plot["encoding"]["x"]["stack"] == "zero"


def test_barh_xy():
    df = pd.DataFrame({"x": [1, 4, 2, 3, 5], "y": [6, 3, 4, 5, 2]})

    plot = df.vgplot.barh(x="x", y="y")
    utils.validate_vegalite(plot)
    assert plot.mark == "bar"
    utils.check_encodings(plot, x="value", y="x", color="variable")
    data = plot.data
    assert set(pd.unique(data["variable"])) == {"y"}
    assert plot["encoding"]["x"]["stack"] is None


def test_barh_xy_stacked():
    df = pd.DataFrame({"x": [1, 4, 2, 3, 5], "y": [6, 3, 4, 5, 2]})

    plot = df.vgplot.barh(x="x", y="y", stacked=True)
    utils.validate_vegalite(plot)
    assert plot.mark == "bar"
    utils.check_encodings(plot, x="value", y="x", color="variable")
    data = plot.data
    assert set(pd.unique(data["variable"])) == {"y"}
    assert plot["encoding"]["x"]["stack"] == "zero"


def test_series_barh():
    ser = pd.Series([4, 5, 4, 5], index=["A", "B", "C", "D"])
    plot = ser.vgplot.barh()
    utils.validate_vegalite(plot)
    assert plot.mark == "bar"
    utils.check_encodings(plot, y="index", x="0")


def test_df_area_simple():
    df = pd.DataFrame({"x": [1, 4, 2, 3, 5], "y": [6, 3, 4, 5, 2]})

    plot = df.vgplot.area()
    utils.validate_vegalite(plot)
    assert plot.mark == "area"
    utils.check_encodings(plot, x="index", y="value",
                          color="variable")
    data = plot.data
    assert set(pd.unique(data["variable"])) == {"x", "y"}
    assert plot["encoding"]["y"]["stack"] == "zero"


def test_df_area_unstacked():
    df = pd.DataFrame({"x": [1, 4, 2, 3, 5], "y": [6, 3, 4, 5, 2]})

    plot = df.vgplot.area(stacked=False)
    utils.validate_vegalite(plot)
    assert plot.mark == "area"
    utils.check_encodings(
        plot, x="index", y="value", color="variable", opacity=utils.IGNORE
    )
    data = plot.data
    assert set(pd.unique(data["variable"])) == {"x", "y"}
    assert plot["encoding"]["y"]["stack"] is None
    assert plot["encoding"]["opacity"]["value"] == 0.7


def test_df_area_xy():
    df = pd.DataFrame({"x": [1, 4, 2, 3, 5], "y": [6, 3, 4, 5, 2], "z": range(5)})

    plot = df.vgplot.area(x="x", y="y")
    utils.validate_vegalite(plot)
    assert plot.mark == "area"
    utils.check_encodings(plot, x="x", y="value", color="variable")
    data = plot.data
    assert set(pd.unique(data["variable"])) == {"y"}
    assert plot["encoding"]["y"]["stack"] == "zero"


def test_df_area_xy_unstacked():
    df = pd.DataFrame({"x": [1, 4, 2, 3, 5], "y": [6, 3, 4, 5, 2], "z": range(5)})

    plot = df.vgplot.area(x="x", y="y", stacked=False)
    utils.validate_vegalite(plot)
    assert plot.mark == "area"
    utils.check_encodings(plot, x="x", y="value", color="variable")
    data = plot.data
    assert set(pd.unique(data["variable"])) == {"y"}
    assert plot["encoding"]["y"]["stack"] is None


def test_series_area():
    ser = pd.Series([3, 2, 3, 2, 3])
    plot = ser.vgplot.area()
    utils.validate_vegalite(plot)
    assert plot.mark == "area"
    utils.check_encodings(plot, x="index", y="0")


@pytest.mark.parametrize("stacked", [True, False])
@pytest.mark.parametrize("histtype", ["bar", "step", "stepfilled"])
def test_df_hist(stacked, histtype):
    df = pd.DataFrame({"x": range(10), "y": range(10)})

    marks = {
        "bar": "bar",
        "step": {"type": "line", "interpolate": "step"},
        "stepfilled": {"type": "area", "interpolate": "step"},
    }

    # bar histogram
    plot = df.vgplot.hist(bins=5, stacked=stacked, histtype=histtype)
    assert plot.mark == marks[histtype]
    if stacked:
        # No default opacity for a stacked histogram
        utils.check_encodings(plot, x="value", y=utils.IGNORE,
                              color="variable")
    else:
        utils.check_encodings(
            plot, x="value", y=utils.IGNORE, color="variable",
            opacity=utils.IGNORE
        )
    assert plot["encoding"]["x"]["bin"] == {"maxbins": 5}
    assert plot["encoding"]["y"]["aggregate"] == "count"
    assert plot["encoding"]["y"]["stack"] == ("zero" if stacked else None)


@pytest.mark.parametrize("histtype", ["bar", "step", "stepfilled"])
def test_series_hist(histtype):
    ser = pd.Series(range(10))

    marks = {
        "bar": "bar",
        "step": {"type": "line", "interpolate": "step"},
        "stepfilled": {"type": "area", "interpolate": "step"},
    }
    plot = ser.vgplot.hist(bins=5, histtype=histtype)
    assert plot.mark == marks[histtype]

    utils.check_encodings(plot, x="0", y=utils.IGNORE)
    assert plot["encoding"]["x"]["bin"] == {"maxbins": 5}
    assert plot["encoding"]["y"]["aggregate"] == "count"


def test_df_hexbin():
    df = pd.DataFrame({"x": range(10), "y": range(10), "C": range(10)})
    gridsize = 10
    plot = df.vgplot.hexbin(x="x", y="y", gridsize=gridsize)
    assert plot.mark == "rect"
    utils.check_encodings(plot, x="x", y="y", color=utils.IGNORE)
    assert plot["encoding"]["x"]["bin"] == alt.Bin(maxbins=gridsize)
    assert plot["encoding"]["y"]["bin"] == alt.Bin(maxbins=gridsize)
    assert plot["encoding"]["color"]["aggregate"] == "count"


def test_df_hexbin_C():
    df = pd.DataFrame({"x": range(10), "y": range(10), "C": range(10)})
    gridsize = 10
    plot = df.vgplot.hexbin(x="x", y="y", C="C", gridsize=gridsize)
    assert plot.mark == "rect"
    utils.check_encodings(plot, x="x", y="y", color="C")
    assert plot["encoding"]["x"]["bin"] == alt.Bin(maxbins=gridsize)
    assert plot["encoding"]["y"]["bin"] == alt.Bin(maxbins=gridsize)
    assert plot["encoding"]["color"]["aggregate"] == "mean"


def test_df_hexbin_Cfunc():
    df = pd.DataFrame({"x": range(10), "y": range(10), "C": range(10)})
    plot = df.vgplot.hexbin(x="x", y="y", C="C", reduce_C_function=min)
    assert plot["encoding"]["color"]["aggregate"] == "min"
    utils.check_encodings(plot, x="x", y="y", color="C")


def test_df_kde():
    df = pd.DataFrame({"x": range(10), "y": range(10)})
    plot = df.vgplot.kde(bw_method="scott")
    assert plot.mark == "line"
    utils.check_encodings(plot, x=" ", y="Density", color=utils.IGNORE)
    data = plot.data
    assert set(pd.unique(data["variable"])) == {"x", "y"}


def test_df_kde_y():
    df = pd.DataFrame({"x": range(10), "y": range(10)})
    plot = df.vgplot.kde(y="y", bw_method="scott")
    assert plot.mark == "line"
    utils.check_encodings(plot, x=" ", y="Density", color=utils.IGNORE)
    data = plot.data
    assert set(pd.unique(data["variable"])) == {"y"}


def test_ser_kde():
    ser = pd.Series(range(10), name="x")
    plot = ser.vgplot.kde(bw_method="scott")
    assert plot.mark == "line"
    utils.check_encodings(
        plot,
        x=' ',
        y='x',
    )
