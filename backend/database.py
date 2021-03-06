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
    db.upsert(tsn, tsnq.id == tsn['id'])
    pass


def transaction_delete(id):
    """
    Mark transaction as deleted
    :param id: Transaction ID of transaction to mark as deleted
    :return: Whether the transaction exists or not
    """
    tsnq = Query()
    if not db.update(set('deleted', True), tsnq.id == id):
        return False
    return True


def transaction_get_all():
    tsnq = Query()
    return db.search((~tsnq.deleted.exists()) | (tsnq.deleted == False))


def transaction_get_by_id(id):
    tsnq = Query()
    return db.get(tsnq.id == id)


# this isn't used at all
def transaction_get_page(page):
    tsns = transaction_get_all()[::-1]
    # TODO maybe make this more efficient someday
    page_model = [tsns[i:i + config['per_page']] for i in range(0, len(tsns), config['per_page'])]
    if 0 <= page < len(page_model):
        return len(page_model), page_model[page]
    return len(page_model), None


def transaction_get_count():
    return len(db)


def account_get_all():
    tsn = transaction_get_all()
    accounts = {}
    for tact in tsn:
        for src in tact['src']:
            accounts[src['account']] = accounts.get(src['account'], 0) - src['amount']
        for dest in tact['dest']:
            accounts[dest['account']] = accounts.get(dest['account'], 0) + dest['amount']
    return [
        {
            'account': name,
            'amount': value
        } for (name, value) in accounts.items() if value != 0]
