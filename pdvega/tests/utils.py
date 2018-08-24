IGNORE = object()


def check_encodings(chart, **fields):
    edict = chart.encoding.to_dict()
    assert set(edict.keys()) == set(fields.keys())
    for encoding, expected_field in fields.items():
        if expected_field is IGNORE:
            continue

        actual_field = edict[encoding]['field']
        if actual_field != expected_field:
            raise ValueError("Expected '{0}' encoding to be '{1}'; got '{2}'"
                             "".format(encoding, expected_field, actual_field))


def get_data(chart):
    return chart.data


def validate_vegalite(chart):
    assert chart.to_dict(validate=True)
