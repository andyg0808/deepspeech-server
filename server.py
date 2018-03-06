import subprocess
import tempfile
import os
from flask import Flask, request
app = Flask(__name__)

@app.route("/", methods=['POST'])
def hello():
    print("Handling request...", request.files)
    if len(request.files) != 1:
        return ""
    else:
        data = request.files['file']
    with tempfile.NamedTemporaryFile() as tempf:
        data.save(tempf)
        with subprocess.Popen(["./native/deepspeech", "models/output_graph.pb", "models/alphabet.txt", tempf.name], stdout=subprocess.PIPE) as proc:
            proc.wait()
            out, _ = proc.communicate()
            return out


@app.route("/test", methods=['POST'])
def test():
    return "sample text"
