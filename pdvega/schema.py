from pkgutil import get_data
from json import loads

VEGALITE_FILE = 'vega-lite-v2.0.4.json'
VEGALITE_SCHEMA = loads(get_data('pdvega', VEGALITE_FILE).decode('utf-8'))
