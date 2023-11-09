import io
from flask import Flask, jsonify, send_file
from flask import request
from flask_cors import cross_origin

import base64
import numpy as np

def readFileStreamAsNdarray(stream):
  return np.asarray(bytearray(stream.read()), dtype=np.uint8)

app = Flask(__name__)

@app.route("/", methods = ["POST"])
@cross_origin(origins=["http://127.0.0.1:5500"], methods=["POST"])
def hello():
  imgA_array = readFileStreamAsNdarray(request.files['img_A'].stream)
  #print(img_A)
  #img_A = request.form['img_A']
  #img_B = request.form['img_B']

  #print(img_A)

  #print(Base64toNdarray(res["result"]))
  print(imgA_array)
  return send_file(
        io.BytesIO(imgA_array),
        mimetype="image/png",
        as_attachment=True,
    )

app.run(debug=True, host='127.0.0.1', port=5000, threaded=True)

