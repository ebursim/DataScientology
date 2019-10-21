import pickle
from flask import Flask
from flask import request
from flask_cors import CORS

app = Flask(__name__)

@app.route('/', methods=['POST'])
def hello_world():
    pipeline = pickle.load(open("pipeline", "rb"))
    return str(pipeline.predict([request.json])[0])

if __name__ == '__main__':
    CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.run()