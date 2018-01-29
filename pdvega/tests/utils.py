import jsonschema

import pandas as pd

from pdvega.schema import VEGALITE_SCHEMA

IGNORE = object()


def check_encodings(spec, **fields):
    assert set(spec['encoding'].keys()) == set(fields.keys())
    for encoding, expected_field in fields.items():
        if expected_field is IGNORE:
            continue
        actual_field = spec['encoding'][encoding]['field']
        if actual_field != expected_field:
            raise ValueError("Expected '{0}' encoding to be '{1}'; got '{2}'"
                             "".format(encoding, expected_field, actual_field))


def get_data(spec):
    return pd.DataFrame.from_records(spec['data']['values'])


def validate_vegalite(spec):
    return jsonschema.validate(spec, VEGALITE_SCHEMA)
