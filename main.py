import json
import os
import time
import md5
from flask import Flask, request, jsonify
import conf

app = Flask(__name__)

# app.debug = True

port = 8918
host = '0.0.0.0'
tmp_dir_name = 'tx_py'

@app.route('/')
def index():
    return 'I\'m ready for that, you know.'

@app.route('/api/update', methods=['POST'])
def update():
    if request.method == 'POST':
        data = request.get_data()
        if data == '':
            return get_wrong_msg('Wrong json string.')
        d = json.loads(data)

        token =  d['auth_token']
        timestamp = d['timestamp']
        isOk = check_token(str(timestamp) + conf.psw, token)
        if not isOk:
            return get_wrong_msg('Wrong token.')

        if 'blackurllist' not in d:
            return get_wrong_msg('No blackurllist data.')
        url_list = d['blackurllist']

        if len(url_list) == 0:
            return get_wrong_msg('No url list data.')

        store_data(url_list)
    return get_ok_state()

def store_data(data):
    rs_path = os.path.join(os.getcwd(), tmp_dir_name)

    # make sure the dir is exist.
    make_sure_dir(rs_path)
    file_path = os.path.join(rs_path, 'url_list_' + time.strftime("%Y%m%d_%H%M%S"))

    fileObject = open(file_path, 'w')
    rs_list = []
    for i in data:
        if i['url'] != '':
            rs_list.append(i['url'])
    
    fileObject.write('\n'.join(rs_list))
    fileObject.close()

def make_sure_dir(path):
    if os.path.isdir(path):
        pass
    else:
        os.mkdir(path)

def check_token(t, token):
    md5_str = get_md5_str(t)
    rs = md5_str[0:16]
    print('rs',rs)
    if rs == token:
        return True
    else:
        return False

def get_md5_str(s):
    m = md5.new()
    m.update(s)
    return m.hexdigest()

def get_wrong_msg(msg):
    rs = {}
    rs['result'] = 'fail'
    rs['msg'] = msg
    return jsonify(rs)

def get_ok_state():
    rs = {}
    rs['result'] = 'ok'
    rs['msg'] = 'ok'
    return jsonify(rs)

if __name__ == '__main__':
    app.run(host=host, port=port)
