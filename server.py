import subprocess
import os
from flask import Flask, request
app = Flask(__name__)

@app.route("/", methods=['POST'])
def hello():
    print(request.files)
    if len(request.files) != 1:
        return ""
    else:
        data = request.files['file']
        print(data.fileno())
    with subprocess.Popen(["bash", "-c", "./native/deepspeech models/output_graph.pb /proc/{}/fd/{} models/alphabet.txt".format(os.getpid(), data.fileno())], stdout=subprocess.PIPE) as proc:
        proc.wait()
        out, _ = proc.communicate()
        return out
        
