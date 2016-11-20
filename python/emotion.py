from __future__ import print_function
import requests
import time


_url = "https://api.projectoxford.ai/emotion/v1.0/recognize"
_key = "b3cb7d20e5d9488199615e7a27a77c14"
_maxNumRetries = 10


class Face:
    def __init__(self, face):
        self.offset = (face["faceRectangle"]["left"] +
                       face["faceRectangle"]["width"] / 2)
        self.scores = face["scores"]


def process_request(json, data, headers, params):
    """Helper function to process the request to MCS.

       :param json: Used when processing images from its URL.
       :param data: Used when processing image read from disk.
       :param headers: Used to pass the key information and
                       the data type request.
    """
    retries = 0
    result = None

    while True:
        response = requests.request("post", _url, json=json,
                                    data=data, headers=headers, params=params)
        if response.status_code == 429:
            if retries <= _maxNumRetries:
                time.sleep(1)
                retries += 1
                continue
            else:
                print("Error: failed after retrying!")
                break
        elif response.status_code == 200 or response.status_code == 201:
            if ("content-length" in response.headers and
               int(response.headers["content-length"]) == 0):
                result = None
            elif ("content-type" in response.headers and
                 isinstance(response.headers["content-type"], str)):
                if ("application/json" in
                   response.headers["content-type"].lower()):
                    result = response.json() if response.content else None
                elif "image" in response.headers["content-type"].lower():
                    result = response.content
        else:
            print("Error code: %d" % response.status_code)
            print("Message: %s" % response.json()["error"]["message"])
        break
    return result


def analyze(image):
    headers = dict()
    headers["Ocp-Apim-Subscription-Key"] = _key
    headers["Content-Type"] = "application/octet-stream"
    raw_data = process_request(None, image, headers, None)
    data = []
    for face in raw_data:
        data.append(Face(face))
    return data
