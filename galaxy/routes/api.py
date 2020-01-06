import json
import os
import secrets
import hashlib

import qiniu
import requests
from PIL import Image
from flask import current_app, Blueprint, request, jsonify
from flask_login import current_user

from .. import db
from ..models.file import File
from galaxy import rest_login_required

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/q-upload', methods=['POST'])
def q_upload():
    if not current_user.is_authenticated:
        return jsonify({"msg": "login required"}), 401
    file = request.files.get('file')
    f_name, f_ext = os.path.splitext(file.filename)
    filename = secrets.token_hex(8) + f_ext
    action = current_app.config['QINIU_ACTION']
    q = qiniu.Auth(current_app.config['QINIU_ACCESS_KEY'], current_app.config['QINIU_SECRET_KEY'])
    token = q.upload_token(current_app.config['QINIU_BUCKET'], filename, 3600)
    files = {
        "file": file
    }
    data = {
        "token": token,
        "key": filename
    }
    r = requests.post(action, files=files, data=data)
    return json.loads(r.text), r.status_code


@api.route('/upload', methods=['POST'])
@rest_login_required
def upload():
    # if not current_user.is_authenticated:
    #     return jsonify({"msg": "login required"}), 401
    file = request.files.get('file')
    if not file:
        return jsonify({'msg': 'need a file to upload'}), 400
    f_name, f_ext = os.path.splitext(file.filename)
    filename = secrets.token_hex(8) + f_ext
    file_path = os.path.join(current_app.root_path, 'static/upload', filename)
    i = Image.open(file)
    md5 = hashlib.md5(i.tobytes()).hexdigest()
    exist_file = File.query.filter_by(md5=md5).first()
    if not exist_file:
        i.save(file_path)
        f = File(original_name=f_name, md5=md5, name=filename, ext=f_ext, create_by=current_user.username)
        db.session.add(f)
        db.session.commit()
    else:
        f_name = exist_file.original_name
        filename = exist_file.name
        f_ext = exist_file.ext
        f = exist_file
    return jsonify({
        "data": {
            "original_name": f_name,
            "name": filename,
            "ext": f_ext,
            "md5": md5,
            "url": request.host_url + 'static/upload/' + filename,
            "timestamp": f.timestamp.strftime('%Y-%m-%d %X')
        },
        "msg": "ok"
    })

