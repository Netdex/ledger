from gevent.pywsgi import WSGIServer
import json
from flask import Flask, request, abort, send_from_directory
from werkzeug.utils import secure_filename
import os
import uuid

import database as db
import validation
from config import config

app = Flask(__name__,
            static_folder="../frontend/dist",
            static_url_path="")

app.config['UPLOAD_FOLDER'] = config['upload_folder']
os.makedirs(config['upload_folder'], exist_ok=True)
app.config['MAX_CONTENT_LENGTH'] = config['max_content_length']




@app.route('/transaction/upsert', methods=['POST'])
def rt_transaction_upsert():
    data = json.loads(request.form.get('data'))
    evidence_paths_list = []
    evidence_names_list = []
    for file in request.files.getlist("evidence[]"):
        if file and validation.validate_file_name(file.filename):
            filename = str(uuid.uuid4()) + '-' + secure_filename(file.filename)
            evidence_paths_list.append(filename)
            evidence_names_list.append(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            return 'a file uploaded was not valid', 400

    if not validation.validate_transaction(data):
        return 'the transaction is not valid', 400
    data['_evidence_paths'] = evidence_paths_list
    data['_evidence_names'] = evidence_names_list
    db.transaction_upsert(data)

    return '', 200


@app.route('/evidence/get/<string:id>')
def rt_evidence_get_by_id(id):
    return send_from_directory(config['upload_folder'], id)


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
