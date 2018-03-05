from flask import Flask, request
import json
import os
import time

app = Flask(__name__)
app.debug = True

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
            return 'Wrong json string.'
        d = json.loads(data)
        if 'blackurllist' not in d:
            return 'No blackurllist data.'
        url_list = d['blackurllist']

        if len(url_list) == 0:
            return 'No url list data.'

        store_data(url_list)
    return 'test'


def store_data(data):
    rs_path = os.path.join(os.getcwd(), tmp_dir_name)
    print(rs_path)

    # make sure the dir is exist.
    make_sure_dir(rs_path)
    file_path = os.path.join(rs_path, 'url_list_' + time.strftime("%Y%m%d_%H%M%S"))

    print(file_path)

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

if __name__ == '__main__':
    app.run(host=host, port=port)