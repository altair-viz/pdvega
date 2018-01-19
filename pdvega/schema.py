from pkgutil import get_data
from json import loads

VEGALITE_SCHEMA = loads(get_data('pdvega', 'vega-lite-v2.0.4.json'))
