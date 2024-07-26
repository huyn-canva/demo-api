from flask import Flask, render_template, request
from auth import Auth
from environment import load_env
from api.connect import get_auth_url

app = Flask(__name__)


ENV = load_env(".env")
authentication = Auth(env=ENV)

@app.route('/')
def index():
    return render_template('index.html', message='Hello, Canva Connect API!')

@app.route("/auth/connect_url", methods=['GET'])
def auth_url():
    return {'url': authentication.get_auth_url()}

@app.route("/oauth/redirect", methods=['POST', 'GET'])
def oauth():
    code = request.args.get('code')
    state = request.args.get('state', default=None)
    print(f"Code: {code}\n State: {state}")
    authentication.get_access_token(code=code, state=state)
    return ('', 200)
