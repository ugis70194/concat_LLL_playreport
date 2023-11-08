# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`

from firebase_functions import https_fn
from firebase_admin import initialize_app
import json

app = initialize_app()

@https_fn.on_request()
def on_request_example(req: https_fn.Request) -> https_fn.Response:
    if req.method != "POST":
        return https_fn.Response("accept method is POST only", 400)
    
    rowData = req.get_json()

    res = {
        "a": rowData["imgA"],
        "b": rowData["imgB"],
    }
    #res = {"concat_img": "base64img"}
    return https_fn.Response(json.dumps(res), 200)