import flask

app = flask.Flask(__name__)

def add_cors(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/')
def root():
    return add_cors(flask.send_from_directory('.', 'index.html'))

@app.route('/add_files/<path:path>')
def send_static(path):
    return add_cors(flask.send_from_directory('add_files', path))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)