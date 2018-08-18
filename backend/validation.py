from jsonschema import validate, ValidationError

import transaction


def validate_transaction(trns):
    """
    Validate specified transaction against transaction schema
    :param trns: Transaction to validate
    :return: Whether the transaction matches the schema
    """
    try:
        validate(trns, transaction.schema)
        return True
    except ValidationError:
        return False
