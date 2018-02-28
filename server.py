import subprocess
import json
import requests
from flask import Flask, request
app = Flask(__name__)

@app.route("/", methods=['POST'])
def hello():
    request.files
    #req = request.get_json()
    #print(request.headers)
    with subprocess.Popen(["bash", "-c", "echo deepspeech models/output_graph.pb file16000.wav models/alphabet.txt"], stdout=subprocess.PIPE) as proc:
        proc.wait()
        out, _ = proc.communicate()
        #return_address = req['return_address']
        return out
    #return json.dumps({"result": "success"})
        
