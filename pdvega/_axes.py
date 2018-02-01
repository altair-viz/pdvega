from vega3 import VegaLite


class Axes(object):
    """Class representing a pdvega plot axes"""
    def __init__(self, spec=None, data=None):
        self.vlspec = VegaLite(spec, data)

    @property
    def spec(self):
        return self.vlspec.spec

    @property
    def spec_no_data(self):
        return {key: val for key, val in self.spec.items() if key != 'data'}

    @property
    def data(self):
        return self.vlspec.data

    def _ipython_display_(self):
        return self.vlspec._ipython_display_()

    def display(self):
        return self.vlspec.display()
