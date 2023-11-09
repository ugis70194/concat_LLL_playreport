# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`

from firebase_functions import https_fn, options
from firebase_admin import initialize_app
import json
import base64

import numpy as np
import cv2

def readFileStreamAsNdarray(stream):
  return np.asarray(bytearray(stream.read()), dtype=np.uint8)

def cv2ImageToBase64Text(img):
  _, encoded = cv2.imencode(".jpg", img)
  return base64.b64encode(encoded).decode("ascii")

def stitchingImg(imgA, imgB):
  diff = abs(imgA - imgB)
  diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
  
  bottom = len(diff) - 1
  
  while(diff[bottom].sum() == 0 and bottom > 0):
      bottom -= 1
  
  top = bottom
  
  while(diff[top].sum() != 0 and top > 0):
      top -= 1
  
  clipedImgA = imgA[top:bottom]
  clipedImgB = imgB[top:bottom]
  
  stitcher = cv2.Stitcher.create(cv2.Stitcher_SCANS)
  status, stitchedImg = stitcher.stitch([clipedImgA, clipedImgB])
  completeImg = np.vstack([imgA[:top], stitchedImg, imgA[bottom+1:-1]])
  
  return completeImg

app = initialize_app()

@https_fn.on_request(
  region='asia-northeast2',
  cors=options.CorsOptions(
    cors_origins=["*"],
    cors_methods=["get", "post"]
  )
)
def stitching(request: https_fn.Request) -> https_fn.Response:
    if request.method != "POST":
        return https_fn.Response("accept method is POST only", 400)
    
    imgA_array = readFileStreamAsNdarray(request.files['img_A'].stream)
    imgA = cv2.imdecode(imgA_array, 1)

    imgB_array = readFileStreamAsNdarray(request.files['img_B'].stream)
    imgB = cv2.imdecode(imgB_array, 1)

    stitched_img = stitchingImg(imgA, imgB)
    
    result_base64_encoded = cv2ImageToBase64Text(stitched_img)
    result = {"result": f"data:image/jpeg;base64,{result_base64_encoded}"}

    return https_fn.Response(json.dumps(result), 200)