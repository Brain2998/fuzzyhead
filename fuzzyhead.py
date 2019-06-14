import flask
import dict
import os
import datetime

app = flask.Flask(__name__)

def add_cors(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/', methods = ['GET', 'POST'])
def root():
    if flask.request.method == 'POST':
        print(flask.request.form)
        fuzzing_dict=flask.request.files['dict']
        print(fuzzing_dict)
        dict_dir=os.path.join(os.path.dirname(os.path.realpath('__file__')), 'divided_dict', flask.request.form['name']+'_'+str(datetime.datetime.now().time()))
        os.makedirs(dict_dir, exist_ok=True)
        dict_name=os.path.join(dict_dir, fuzzing_dict.filename)
        fuzzing_dict.save(dict_name)
        dict.divide_dict(dict_name, int(flask.request.form['divide_dict']))

    return add_cors(flask.send_from_directory('.', 'index.html'))

@app.route('/add_files/<path:path>')
def send_static(path):
    return add_cors(flask.send_from_directory('add_files', path))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)