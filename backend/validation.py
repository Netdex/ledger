from jsonschema import validate, ValidationError
from functools import reduce

import transaction
from config import config


def validate_file_name(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config['allowed_ext']


def validate_transaction(tact):
    """
    Validate specified transaction against transaction schema
    :param tact: Transaction to validate
    :return: Whether the transaction matches the schema
    """
    try:
        # validate transaction against JSON schema
        validate(tact, transaction.schema)

        # validate that src and dest are balanced
        def transaction_srcdest_total(tactlist):
            return reduce((lambda acc, x: acc + x['amount']), tactlist, 0)

        if transaction_srcdest_total(tact['src']) != transaction_srcdest_total(tact['dest']):
            return False

        return True
    except ValidationError as e:
        print(e)
    return False
