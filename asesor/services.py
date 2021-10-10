from typing import Any, Dict
import requests

def generate_request(url:str, params:Dict, verb:str = "GET")-> Any:
    response = requests.get(url, params) if verb == "GET" else requests.post(url, params)
    return response.json()

def obtener_datos(params:Dict,verb:str = "GET")-> Any:
    defaultParams:Dict = {
        "wstoken": "cae40824ddd52a292888f736c8843929",
        "moodlewsrestformat": "json"
    }
    defaultParams.update(params)
    response:Any=generate_request("http://academyec.com/moodle/webservice/rest/server.php",defaultParams, verb)
    return response