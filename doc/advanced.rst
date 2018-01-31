.. _advanced-plotting:

Advanced Plotting: Using Vega-Lite Directly
===========================================

The ``pdvega`` API is rather simplistic at the moment; it doesn't give easy
access to many of the features that Vega-Lite supports.
In the future, we would like to tie ``pdvega`` to the `Altair`_ project, which
would allow plot outputs to be adjusted flexibly from within a Python API.

In the meantime, it is possible to make more fine-tuned adjustments to your
plot specifications by working directly in the specification dictionary.

For example, consider this plot:

.. pdvega-setup::

   import pdvega
   import pandas

.. pdvega-plot::

   from vega_datasets import data
   iris = data.iris()

   iris.vgplot(kind='scatter', x='sepalLength', y='petalLength', c='species')

Vega-Lite's default behavior is to include the zero-value in the scale, unless
the user explicitly turns that requirement off in the JSON spec.

``pdvega`` is not designed to give easy access to every option available in the
Vega-Lite schema, but it is possible to modify the specification manually.
We can access the raw Vega-Lite specification from any plot using the ``spec``
attribute. For convenience, there is also a ``spec_no_data`` attribute that
returns the spec without the the embedded data:

.. code-block:: python

   >>> plot = iris.vgplot(kind='scatter', x='sepalLength', y='petalLength', c='species')
   >>> plot.spec_no_data
   {'$schema': 'https://vega.github.io/schema/vega-lite/v2.json',
   'encoding': {'color': {'field': 'species', 'type': 'nominal'},
    'x': {'field': 'sepalLength', 'type': 'quantitative'},
    'y': {'field': 'petalLength', 'type': 'quantitative'}},
   'height': 300,
   'mark': 'circle',
   'selection': {'grid': {'bind': 'scales', 'type': 'interval'}},
   'width': 450}

This dictionary contains the specification that tells the vega-lite renderer
how to map data to visual components in the plot. You can read more details on
the `Vega-Lite`_ website. In particular, if you look at the options for
`Vega-Lite scales`_, you can see that there is a ``"scale"`` property of the "x"
encoding which allows turning off the zero behavior.
Knowing this, we can update the specification manually to get the desired result:

.. pdvega-setup::

    from vega_datasets import data
    iris = data.iris()
    plot = iris.vgplot(kind='scatter', x='sepalLength', y='petalLength', c='species')

.. pdvega-plot::

    plot.spec['encoding']['x']['scale'] = {'zero': False}
    plot

Using this type of approach, you can customize your plots in any way that Vega-Lite
allows.

This is admittedly a bit of a clumsy solution for plot customization; mucking around
in the internals of the JSON specification requires a deep knowledge of the vega-lite
schema, and the renderer is not very forgiving if and when you
make an error or typo.
In the future, we plan to make ``pdvega`` plots output `Altair`_
objects, which will allow this sort of customization to be done much more cleanly
with Altair's Python API.

Skipping ``vgplot`` entirely
----------------------------
If you would like to skip pdvega's vgplot API entirely and build your Vega-Lite plot
from scratch, pdvega's :class:`~pdvega.VegaLiteAxes` object lets you do this directly.
For example:

.. pdvega-plot::

   from pdvega import VegaLiteAxes

   spec = {
     '$schema': 'https://vega.github.io/schema/vega-lite/v2.json',
     'mark': 'point',
     'encoding': {
       'color': {'field': 'species', 'type': 'nominal'},
       'x': {'field': 'petalWidth', 'type': 'quantitative'},
       'y': {'field': 'petalLength', 'type': 'quantitative'}
     },
     'height': 300,
     'width': 450,
     # this selection is what makes the plot interactive
     'selection': {'grid': {'bind': 'scales', 'type': 'interval'}},
   }

   # Build the vgplot specification
   VegaLiteAxes(spec, iris)

For ideas on what sort of visualizations you can create in this way,
check out the specifications on the `Vega-Lite examples`_ page.
The `Vega online editor`_ is also a useful resource for developing visualizations
directly in Vega or Vega-Lite.

.. _Vega-Lite: http://vega.github.io/vega-lite/
.. _Altair: http://altair-viz.github.io/
.. _Vega-Lite scales: https://vega.github.io/vega-lite/docs/scale.html
.. _Vega-Lite examples: https://vega.github.io/vega-lite/examples/
.. _Vega online editor: https://vega.github.io/editor/#/custom/vega-lite
