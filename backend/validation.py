from jsonschema import validate, ValidationError
from functools import reduce

import transaction


def validate_transaction(trns):
    """
    Validate specified transaction against transaction schema
    :param trns: Transaction to validate
    :return: Whether the transaction matches the schema
    """
    try:
        validate(trns, transaction.schema)
        if reduce((lambda acc, x: acc + x['amount']), trns['src'], 0) \
                != reduce((lambda acc, x: acc + x['amount']), trns['dest'], 0):
            return False
        return True
    except ValidationError as e:
        print(e)
    return False
