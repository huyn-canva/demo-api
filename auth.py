import secrets
import pkce
import requests
from requests.auth import HTTPBasicAuth
from environment import Environment
from urllib.parse import urlencode
import hashlib
from pprint import pprint


from typing import Optional
from base64 import b64encode

AUTH_URL="https://www.canva.com/api/oauth/authorize"

class Auth():
    credentials: str 
    client_id: str
    redirect_uri: str = None
    code_verifier: str = None
    code_challenge: str = None
    state: str = None
    code: str = None
    access_token: str = None
    refresh_token: str = None

    def __init__(self, env: Environment):
        self.client_id = env.client_id
        self.redirect_uri = env.redirect_uri
        self.credentials = b64encode(f"{env.client_id}:{env.client_secret}".encode()).decode()
        self.code_verifier, self.code_challenge = pkce.generate_pkce_pair(96)
        self.state = secrets.token_urlsafe(96)


    def get_auth_url(self) -> str:
        params={
            "code_challenge_method": "s256",
            "response_type": "code",
            "client_id": self.client_id,
            "code_challenge": self.code_challenge,
            "state": self.state,
            "scope": "folder:read folder:write asset:read asset:write",
        }
        if self.redirect_uri:
            params["redirect_uri"] = self.redirect_uri

        url = f"{AUTH_URL}?{urlencode(params)}"
        print(url)
        return url

    def get_access_token(self, code: str, state: Optional[str] = None) -> None:
        self.code = code
        if state and state != self.state:
            print(f"State {state} is not the same as initial state {self.state}")

        headers = {
            "Authorization": "Basic %s" % self.credentials,
            "Content-Type": "application/x-www-form-urlencoded"
        }

        data = {
            "grant_type": "authorization_code",
            "code_verifier": self.code_verifier,
            "code": self.code,
            "redirect_uri": self.redirect_uri,
        }

        response = requests.post("https://api.canva.com/rest/v1/oauth/token",
            headers=headers,
            data=data
        )
        pprint(curlify(response.request))
        if response.ok: 
            json = response.json()
            self.access_token = json["access_token"]
            self.refresh_token = json["refresh_token"]
        else:
            print(f"status code: {response.status_code}")
            json = response.json()
            pprint(json)

def curlify(req) -> str:
    command = "curl -X {method} -H {headers} -d '{data}' '{uri}'"
    method = req.method
    uri = req.url
    data = req.body
    headers = ['"{0}: {1}"'.format(k, v) for k, v in req.headers.items()]
    headers = " -H ".join(headers)
    return command.format(method=method, headers=headers, data=data, uri=uri)

