from gevent.pywsgi import WSGIServer
import json
from flask import Flask, request, abort

import database as db
import validation
from config import config

app = Flask(__name__,
            static_folder="../frontend/dist",
            static_url_path="")


@app.route('/transaction/upsert', methods=['POST'])
def rt_transaction_upsert():
    data = request.get_json()
    if not validation.validate_transaction(data):
        abort(400)
    db.transaction_upsert(data)
    return '', 200


@app.route('/transaction/get/<string:id>')
def rt_transaction_get_by_id(id):
    return json.dumps(db.transaction_get_by_id(id))


@app.route('/transaction/get/all')
def rt_transaction_get_all():
    # assumption: database maintains insertion order
    return json.dumps(db.transaction_get_all()[::-1])


@app.route('/transaction/get/page/<int:page>')
def rt_transaction_get_page(page):
    pages, page_obj = db.transaction_get_page(page)

    return json.dumps({
        'page_count': pages,
        'total': db.transaction_get_count(),
        'per_page': config['per_page'],
        'page': page_obj
    })


@app.route('/transaction/delete/<string:id>')
def rt_transaction_delete(id):
    db.transaction_delete(id)
    return '', 200


@app.route('/')
def rt_index():
    return app.send_static_file("index.html")


if __name__ == '__main__':
    if config['devel']:
        app.run()
    else:
        http_server = WSGIServer(('', config['port']), app)
        http_server.serve_forever()
