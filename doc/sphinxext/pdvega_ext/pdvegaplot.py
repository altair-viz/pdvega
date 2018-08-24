"""
PdVega Plot Sphinx Extension
============================

This extension provides a means of inserting live-rendered PdVega plots within
sphinx documentation. There are two directives defined: ``pdvega-setup`` and
``altiar-plot``. ``pdvega-setup`` code is used to set-up various options
prior to running the plot code. For example::

    .. pdvega-setup::

        import pdvega
        import pandas as pd
        data = pd.Series([1, 2, 3, 2, 1, 2, 3])

    .. pdvega-plot::

        data.plot.line()


In the case of the ``pdvega-plot`` code, the *last statement* of the code-block
should evaluate to a pdvega Axes object.

Options
-------
The directives have the following options::

    .. pdvega-setup::
        :show: # if set, then show the setup code as a code block

        pass

    .. pdvega-plot::
        :hide-code:  # if set, then hide the code and only show the plot
        :code-below:  # if set, then code is below rather than above the figure
        :alt: text  # Alternate text when plot cannot be rendered
        :links: editor source export  # specify one or more of these options

        Chart()

Additionally, this extension introduces a global configuration
``pdvegaplot_links``, set in your ``conf.py`` which is a dictionary
of links that will appear below plots, unless the ``:links:`` option
again overrides it. It should look something like this::

    # conf.py
    # ...
    pdvegaplot_links = {'editor': True, 'source': True, 'export': True}
    # ...

If this configuration is not specified, all are set to True.
"""

import os
import json
import warnings

import jinja2

from docutils import nodes
from docutils.parsers.rst import Directive
from docutils.parsers.rst.directives import flag, unchanged

from sphinx.locale import _

from pdvega import Axes
from .utils import exec_then_eval

# These default URLs can be changed in conf.py; see setup() below.
VEGA_JS_URL_DEFAULT = "https://cdn.jsdelivr.net/npm/vega"
VEGALITE_JS_URL_DEFAULT = "https://cdn.jsdelivr.net/npm/vega-lite"
VEGAEMBED_JS_URL_DEFAULT = "https://cdn.jsdelivr.net/npm/vega-embed"


VGL_TEMPLATE = jinja2.Template("""
<div id="{{ div_id }}">
<script>
  // embed when document is loaded, to ensure vega library is available
  // this works on all modern browsers, except IE8 and older
  document.addEventListener("DOMContentLoaded", function(event) {
    vegaEmbed("#{{ div_id }}", "{{ url }}").then(function(result) {
      console.log(result);
    }).catch(console.error);
  });
</script>
</div>
""")


class pdvega_plot(nodes.General, nodes.Element):
    pass


class PdVegaSetupDirective(Directive):
    has_content = True

    option_spec = {'show': flag}

    def run(self):
        env = self.state.document.settings.env

        targetid = "pdvega-plot-{0}".format(env.new_serialno('pdvega-plot'))
        targetnode = nodes.target('', '', ids=[targetid])

        code = '\n'.join(self.content)

        # Here we cache the code for use in later setup
        if not hasattr(env, 'pdvega_plot_setup'):
            env.pdvega_plot_setup = []
        env.pdvega_plot_setup.append({
            'docname': env.docname,
            'lineno': self.lineno,
            'code': code,
            'target': targetnode,
        })

        result = [targetnode]

        if 'show' in self.options:
            source_literal = nodes.literal_block(code, code)
            source_literal['language'] = 'python'
            result.append(source_literal)

        return result


def purge_pdvega_plot_setup(app, env, docname):
    if not hasattr(env, 'pdvega_plot_setup'):
        return
    env.pdvega_plot_setup = [item for item in env.pdvega_plot_setup
                             if item['docname'] != docname]


DEFAULT_PDVEGAPLOT_LINKS = {'editor': True, 'source': True, 'export': True}


def validate_links(links):
    if links.strip().lower() == 'none':
        return {}

    links = links.strip().split()
    diff = set(links) - set(DEFAULT_PDVEGAPLOT_LINKS.keys())
    if diff:
        raise ValueError("Following links are invalid: {0}".format(list(diff)))
    return dict((link, link in links) for link in DEFAULT_PDVEGAPLOT_LINKS)


class PdVegaPlotDirective(Directive):

    has_content = True

    option_spec = {'hide-code': flag,
                   'code-below': flag,
                   'alt': unchanged,
                   'links': validate_links}

    def run(self):
        env = self.state.document.settings.env
        app = env.app

        show_code = 'hide-code' not in self.options
        code_below = 'code-below' in self.options

        setupcode = '\n'.join(item['code']
                              for item in getattr(env, 'pdvega_plot_setup', [])
                              if item['docname'] == env.docname)

        code = '\n'.join(self.content)

        if show_code:
            source_literal = nodes.literal_block(code, code)
            source_literal['language'] = 'python'

        #get the name of the source file we are currently processing
        rst_source = self.state_machine.document['source']
        rst_dir = os.path.dirname(rst_source)
        rst_filename = os.path.basename(rst_source)

        # use the source file name to construct a friendly target_id
        serialno = env.new_serialno('pdvega-plot')
        rst_base = rst_filename.replace('.', '-')
        div_id = "{0}-pdvega-plot-{1}".format(rst_base, serialno)
        target_id = "{0}-pdvega-source-{1}".format(rst_base, serialno)
        target_node = nodes.target('', '', ids=[target_id])

        # create the node in which the plot will appear;
        # this will be processed by html_visit_pdvega_plot
        plot_node = pdvega_plot()
        plot_node['target_id'] = target_id
        plot_node['div_id'] = div_id
        plot_node['code'] = code
        plot_node['setupcode'] = setupcode
        plot_node['relpath'] = os.path.relpath(rst_dir, env.srcdir)
        plot_node['rst_source'] = rst_source
        plot_node['rst_lineno'] = self.lineno
        plot_node['links'] = self.options.get('links', app.builder.config.pdvegaplot_links)
        plot_node['url_root'] = app.config.pdvegaplot_url_root

        if 'alt' in self.options:
            plot_node['alt'] = self.options['alt']

        result = [target_node]

        if code_below:
            result += [plot_node]
        if show_code:
            result += [source_literal]
        if not code_below:
            result += [plot_node]

        return result


def html_visit_pdvega_plot(self, node):
    # Execute the setup code, saving the global & local state

    namespace = {}
    if node['setupcode']:
        exec(node['setupcode'], namespace)

    # Execute the plot code in this context, evaluating the last line
    try:
        output = exec_then_eval(node['code'], namespace)
    except Exception as e:
        warnings.warn("pdvega-plot: {0}:{1} Code Execution failed:"
                      "{2}: {3}".format(node['rst_source'], node['rst_lineno'],
                                        e.__class__.__name__, str(e)))
        raise nodes.SkipNode

    if isinstance(output, Axes):
        # Last line should be a Vega-Lite chart; get the spec:
        spec = output.spec

        # Create the vega-lite spec to embed
        # embed_spec = json.dumps({'mode': 'vega-lite',
        #                          'actions': node['links'],
        #                          'spec': spec})

        # Previously we did this, but after github migrated to https only
        # it started causing issues for some http clients such as localhost.
        #embed_spec = embed_spec.replace('http://', '//')
        #embed_spec = embed_spec.replace('https://', '//')

        # Write embed_spec to a *.vl.json file
        dest_dir = os.path.join(self.builder.outdir, node['relpath'])
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        filename = "{0}.vl.json".format(node['div_id'])
        # TODO: let this url be configured
        url = "{0}{1}.vl.json".format(node['url_root'], node['div_id'])
        dest_path = os.path.join(dest_dir, filename)
        with open(dest_path, 'w') as f:
            json.dump(spec, f)

        # Pass relevant info into the template and append to the output
        html = VGL_TEMPLATE.render(div_id=node['div_id'], url=url)
        self.body.append(html)
    else:
        warnings.warn('pdvega-plot: {0}:{1} Malformed block. Last line of '
                      'code block should define a valid pdvega object.'
                      ''.format(node['rst_source'], node['rst_lineno']))
    raise nodes.SkipNode


def generic_visit_pdvega_plot(self, node):
    # TODO: generate PNGs and insert them here
    if 'alt' in node.attributes:
        self.body.append(_('[ graph: %s ]') % node['alt'])
    else:
        self.body.append(_('[ graph ]'))
    raise nodes.SkipNode


def builder_inited(app):
    app.add_javascript(app.config.pdvegaplot_vega_js_url)
    app.add_javascript(app.config.pdvegaplot_vegalite_js_url)
    app.add_javascript(app.config.pdvegaplot_vegaembed_js_url)


def setup(app):
    setup.app = app
    setup.config = app.config
    setup.confdir = app.confdir

    app.add_config_value('pdvegaplot_links', DEFAULT_PDVEGAPLOT_LINKS, 'env')

    app.add_config_value('pdvegaplot_vega_js_url', VEGA_JS_URL_DEFAULT, 'html')
    app.add_config_value('pdvegaplot_vegalite_js_url', VEGALITE_JS_URL_DEFAULT, 'html')
    app.add_config_value('pdvegaplot_vegaembed_js_url', VEGAEMBED_JS_URL_DEFAULT, 'html')

    app.add_config_value('pdvegaplot_url_root', '/', 'html')

    app.add_directive('pdvega-plot', PdVegaPlotDirective)
    app.add_directive('pdvega-setup', PdVegaSetupDirective)

    app.add_stylesheet('pdvega-plot.css')

    app.add_node(pdvega_plot,
                 html=(html_visit_pdvega_plot, None),
                 latex=(generic_visit_pdvega_plot, None),
                 texinfo=(generic_visit_pdvega_plot, None),
                 text=(generic_visit_pdvega_plot, None),
                 man=(generic_visit_pdvega_plot, None))

    app.connect('env-purge-doc', purge_pdvega_plot_setup)
    app.connect('builder-inited', builder_inited)

    return {'version': '0.1'}
