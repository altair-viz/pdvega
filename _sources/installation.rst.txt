.. _installation:

Installing and Using ``pdvega``
===============================

To install and use ``pdvega`` run the following commands:

.. code-block:: bash

    $ pip install pdvega
    $ jupyter nbextension install --sys-prefix --py vega3

The first command installs the `pdvega <https://pypi.python.org/pypi/pdvega>`_
Python package along with its dependencies (`Pandas`_ and `vega3`_).
The second command above installs the `vega3`_ Jupyter notebook extension, which
is required for ``pdvega`` plots to display automatically in the notebook.

Using ``pdvega`` in the Jupyter Notebook
----------------------------------------
When ``pdvega`` and ``vega3`` are correctly installed, you can create a
visualization within the Jupyter notebook by executing a cell with a plot
command as the last statement in the cell. For example:

.. pdvega-plot::

   import pandas as pd
   import pdvega  # adds vgplot attribute to Pandas objects

   data = pd.Series([1,2,3,2,3,4,3,4,5])
   data.vgplot()

You can also explicitly call the ``plot.display()`` method to display a plot
saved in a variable:

.. code-block:: python

   plot = data.vgplot()
   plot.display()

.. pdvega-plot::
    :hide-code:

    import pandas as pd
    import pdvega  # adds vgplot attribute to Pandas objects

    data = pd.Series([1,2,3,2,3,4,3,4,5])
    data.vgplot()


Using ``pdvega`` Outside Jupyter
--------------------------------
If you wish to use ``pdvega`` outside the Jupyter notebook, you can save the
plot specification to a JSON file:

.. code-block:: python

    import json
    plot = data.vgplot()
    json.dump(plot.spec, 'plot.json')

The resulting plot specification can then be rendered within an HTML page
using the `vega-embed`_ Javascript package.

Saving Visualizations to PNG or SVG
-----------------------------------
To save a visualization to PNG, you can use the link generated below the
rendered plot. Programmatic saving of figures is not currently supported
from within Python, though it is possible using the ``vl2png`` and ``vl2svg``
command-line tools provided in the `vega-lite`_ npm package.


.. _Jupyter notebook: http://jupyter.org/
.. _Pandas: http://pandas.pydata.org/
.. _vega3: http://pypi.python.org/pypi/vega3/
.. _vega-embed: https://vega.github.io/vega-lite/usage/embed.html
.. _vega-lite: https://github.com/vega/vega-lite
