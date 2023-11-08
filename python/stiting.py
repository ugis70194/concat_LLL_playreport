from firebase_functions import https_fn
from firebase_admin import initialize_app
import flask
from flask_cors import CORS

import cv2
import numpy as np

initialize_app()
app = flask.Flask(__name__)

def imread(req: https_fn.Request, id: str):
  if not req.files[id]:
    return []
  
  stream = req.files[id].stream
  img_array = np.asarray(bytearray(stream.read()), dtype=np.uint8)
  return cv2.imdecode(img_array, 1)

def main(req: https_fn.Request) -> https_fn.Response:
  imgA = cv2.imread('./B.jpg')
  imgB = cv2.imread('./C.jpg')

  # 二枚の画像の差分を取る
  # 共通している部分 = スキル発動回数以外の部分はいらないので切り抜く
  diff = abs(imgA - imgB)
  diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
  
  height = len(diff)
  
  top = 0
  bottom = len(diff) - 1
  
  while(diff[top].sum() == 0 and top < height):
      top += 1
  
  while(diff[bottom].sum() == 0 and bottom > 0):
      bottom -= 1

  clipedImgA = imgA[top:bottom]
  clipedImgB = imgB[top:bottom]

  # 画像の連結
  stitcher = cv2.Stitcher.create(cv2.Stitcher_SCANS)
  status, stitchedImg = stitcher.stitch([clipedImgA, clipedImgB])

  completeImg = np.vstack([imgA[:top], stitchedImg, imgA[bottom:-1]])

  cv2.imwrite('./stitched.jpg', completeImg)


if __name__ == '__main__':
  main()