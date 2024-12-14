"""Api interface with the xray-atlas website."""

import requests
from xray_atlas.server.db import DataSet, Molecule, Uid

INVOKE_URL = "https://bfsd0tdg6f.execute-api.us-west-2.amazonaws.com/prod"


class Verb:
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


class ApiRequest:
    def __init__(self, verb, path):
        self.verb = verb
        self.path = path


def fetch_api(request):
    path = f"{INVOKE_URL}/{request.path}"
    response = requests.request(method=request.verb, url=path).json()
    return response


def get_molecules() -> list[Molecule]:
    request = ApiRequest(Verb.GET, "bucket/molecules")
    response = fetch_api(request)
    return response.get("molecules", [])


def get_molecule(name) -> Molecule:
    path = f"bucket/molecules/{name.upper().replace(' ', '')}/metadata"
    request = ApiRequest("GET", path)
    response = fetch_api(request)
    return response.get("molecule", {})


def get_dataset(name, exp) -> DataSet:
    uid = Uid(exp)
    path = f"bucket/molecules/{name.upper().replace(' ', '')}/{uid}"
    request = ApiRequest(Verb.GET, path)
    response = fetch_api(request)
    return response
