from tinydb import TinyDB, Query
from tinydb.operations import set
import uuid

from config import config

db = TinyDB(config['db_path'])


def transaction_upsert(tsn):
    """
    Upsert transaction into database
    :param tsn: Verified transaction to upsert
    """
    # if no ID is given, generate a new ID for insert
    if not tsn.get('id'):
        tsn.update({'id': str(uuid.uuid4())})

    tsnq = Query()
    db.upsert(tsn, tsnq.id == tsn.id)
    pass


def transaction_delete(tsn_id):
    """
    Mark transaction as deleted
    :param tsn_id: Transaction ID of transaction to mark as deleted
    :return: Whether the transaction exists or not
    """
    tsnq = Query()
    if not db.update(set('deleted', True), tsnq.id == tsn_id):
        return False
    return True

def transaction_get_all():

