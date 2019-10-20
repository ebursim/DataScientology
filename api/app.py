import pickle
from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/')
def hello_world():
    pipeline = pickle.load(open("pipeline", "rb"))
    return str(int(pipeline.predict([[x % 2 for x in range (0, 236)]])[0]))

if __name__ == '__main__':
    app.run(debug=True)