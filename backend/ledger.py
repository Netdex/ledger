from flask import Flask, render_template, request, abort
import json
from datetime import datetime
import uuid

import validation
import database as db

app = Flask(__name__)


@app.route('/')
def rt_index():
    return render_template('index.html')


@app.route('/transaction/upsert/<string:id>', methods=['POST'])
def rt_transaction_upsert():
    data = json.loads(request.get_json())
    if not validation.validate_transaction(data):
        abort(400)
    db.transaction_upsert(data)



@app.route('/transaction/get/all')
def rt_transaction_get_all():
    pass


@app.route('/transaction/delete/<string:id>')
def rt_transaction_delete(id):
    pass


if __name__ == '__main__':
    app.run()
