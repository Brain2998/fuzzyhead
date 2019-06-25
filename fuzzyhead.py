import flask
import dict
import os
import datetime
import sqlite3

app = flask.Flask(__name__)
conn = sqlite3.connect('task.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS tasks (id text PRIMARY KEY, name text NOT NULL, 
    dict_path text NOT NULL, fuzzer text NOT NULL, target_ip text NOT NULL, divide_number integer, 
    cli_args text);""")
cursor.execute("""CREATE TABLE IF NOT EXISTS dicts (task_id text, dict_id text, dict_name text NOT NULL,
    PRIMARY KEY(task_id, dict_id));""")
conn.commit()

def add_cors(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/', methods = ['GET', 'POST'])
def root():
    if flask.request.method == 'POST':
        fuzzing_dict=flask.request.files['dict']
        dict_name=fuzzing_dict.filename
        task_name=flask.request.form['name']
        divide_number=int(flask.request.form['divide_number'])

        task_id=task_name+'_'+str(datetime.datetime.now().time())
        #directory to save dictionary to
        dict_dir=os.path.join(os.path.dirname(os.path.realpath('__file__')), 
        'divided_dict', task_id)
        os.makedirs(dict_dir, exist_ok=True)
        #dictionary file inside created directory
        dict_path=os.path.join(dict_dir, dict_name)
        
        cursor.execute('INSERT INTO tasks VALUES (?, ?, ?, ?, ?, ?, ?)', 
        (task_id, task_name, dict_name, flask.request.form['fuzzer'], 
        flask.request.form['target_ip'], divide_number, flask.request.form['cli_args']))
        conn.commit()
        
        fuzzing_dict.save(dict_path)
        dict.divide_dict(dict_path, divide_number, task_id, dict_name)

    return add_cors(flask.send_from_directory('.', 'index.html'))


@app.route('/add_files/<path:path>')
def send_static(path):
    return add_cors(flask.send_from_directory('add_files', path))

@app.route('/fonts/<path:path>')
def send_fonts(path):
    return add_cors(flask.send_from_directory('fonts', path))


@app.route('/getDictById')
def returnDictById():
    args=flask.request.args
    return add_cors(flask.send_from_directory('fonts', path))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)