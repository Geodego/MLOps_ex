from flask import Flask, request
import pandas as pd

app = Flask(__name__)


def readpandas(filename):
    return pd.read_csv('./' + filename)


@app.route('/')
def index():
    user = request.args.get('user')
    return "Hello " + user + '\n'


@app.route('/size')
def size():
    filename = request.args.get('filename')
    df = readpandas(filename)
    return str(df.shape[0]) + '\n'


@app.route('/summary')
def summary():
    filename = request.args.get('filename')
    df = readpandas(filename)
    return str(df.mean(axis=0)) + '\n'


app.run(host='0.0.0.0', port=8000)



