from flask import Flask, render_template, request
import random
import json
import time

a = []
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/boom')
def boom_trigger():
    initiate_launch()
    return json.dumps([1,2,3])

@app.route('/newdata', methods=['POST'])
def newdata():
    global a
    a.extend(map(lambda s: [float(s[0]), float(s[1])],
             json.loads(request.data)))
    return a

def initiate_launch():
    # tell pi to trigger solid state relay
    # note time
    # probably call from different script
    pass

@app.route('/getdata', methods=['GET'])
def getdata():
    global a
    return json.dumps(a)

app.run(host= '0.0.0.0')
