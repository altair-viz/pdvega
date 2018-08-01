import altair as alt


class MaxRowsExceeded(ValueError):
    _msg_template = ("Number of rows in data ({0}) is larger than the maximum "
    "allowed (ax.max_rows={1}). Such large dataframes can cause issues when "
    "the data is embedded for viewing. If you wish to override this, you can "
    "set the ``max_rows`` attribute of your plot Axes instance to a larger "
    "number. For example:\n\n"
    "  ax = data.vgplot.line()\n"
    "  ax.max_rows = {0}\n"
    "  ax.display()\n")
    def __init__(self, rows, rows_max):
        msg = self._msg_template.format(rows, rows_max)
        super(MaxRowsExceeded, self).__init__(msg)


class Axes(object):
    """Class representing a pdvega plot axes"""
    max_rows = 10000  # default value; can be overridden by the class instances

    def __init__(self, spec=None, data=None):
        self._spec = spec or {}
        self._data = data

        if spec is not None:
            # If spec is specified, we need to immediately instantiate the
            # VegaLite object, because it will make some modifications to
            # the spec that we'd like to be able to see by doing ax.spec
            self._vlspec = VegaLite(spec, data)
        else:
            # If the spec is not specified, we set the vegalite object to None
            # and compute it on demand. This allows us to instantiate an empty
            # axis and build from there.
            self._vlspec = None

    @property
    def spec(self):
        if self._vlspec is not None:
            return self._vlspec.spec
        else:
            return self._spec

    @spec.setter
    def spec(self, spec):
        if self._vlspec is not None:
            self._vlspec.spec = spec
        else:
            # if we are setting the spec, then we can instantiate the
            # VegaLite object.
            self._spec = spec
            self._vlspec = VegaLite(self._spec, self._data)

    @property
    def data(self):
        if self._vlspec is not None:
            return self._vlspec.data
        else:
            return self._data

    @data.setter
    def data(self, data):
        if self._vlspec is not None:
            self._vlspec.data = data
        else:
            self._data = data

    @property
    def spec_no_data(self):
        return {key: val for key, val in self.spec.items() if key != 'data'}

    def _check_max_rows(self):
        """
        Ensure that the number of rows in the largest dataset embedded in the
        spec or its layers is smaller than self.max_rows, which defaults to
        10000 unless overridden by the Axes instance.

        Raises
        ------
        MaxRowsExceeded :
            if the dataset is too large.
        """
        nrows = 0
        specs = [self.spec] + self.spec.get('layer', [])
        for spec in specs:
            if 'data' in spec and 'values' in spec['data']:
                nrows = max(nrows, len(spec['data']['values']))
        if nrows > self.max_rows:
            raise MaxRowsExceeded(nrows, self.max_rows)

    def _ipython_display_(self):
        if self._vlspec is None:
            self._vlspec = VegaLite(self._spec, self._data)
        # check max rows after VegaLite modifies the spec
        self._check_max_rows()
        return self._vlspec._ipython_display_()

    def display(self):
        if self._vlspec is None:
            self._vlspec = VegaLite(self._spec, self._data)
        # check max rows after VegaLite modifies the spec
        self._check_max_rows()
        return self._vlspec.display()

    def _add_layer(self, spec, data=None):
        """Add spec as a layer to the current axes.

        Parameters
        ----------
        spec : dictionary
            the spec to be added. If this is the first spec in the axis, every
            part of it will be added. Otherwise, only the 'encoding', 'mark',
            and 'data', 'transform', and 'description' attributes will be added.
        data : dataframe, optional
            if specified, add this data to the layer.

        Returns
        -------
        self : Axes instance
        """
        spec = VegaLite(spec, data).spec
        if not self.spec:
            # current axes spec is empty; replace it entirely with the new one
            self.spec = spec
        else:
            if 'layer' not in self.spec:
                # current axes spec is unlayered; move it to a layer
                keys = ['encoding', 'mark', 'data', 'transform', 'description', 'selection']
                self.spec['layer'] = [{key: self.spec.pop(key)
                                       for key in keys if key in self.spec}]
            # Competing selections in a single layer cause problems, so we
            # limit selections to the first layer for simplicity.
            keys = ['encoding', 'mark', 'data', 'transform', 'description']
            self.spec['layer'].append({key: spec[key]
                                       for key in keys if key in spec})
        # TODO: vega/vega3 raises an error without data defined at top level.
        # This needs an upstream fix; in the meantime we get around it this way:
        if 'data' not in self.spec:
            self.spec['data'] = {'name': 'no-toplevel-data'}
        return self
