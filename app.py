from flask import Flask, render_template, request, redirect
from api.connect import CanvaClient 
from auth import Auth
from environment import load_env

app = Flask(__name__)


ENV = load_env(".env")
authentication = Auth(env=ENV)

@app.route('/')
def index():
    return render_template('index.html', message='Hello, Canva Connect API!')

@app.route("/auth/connect_url", methods=['GET'])
def auth_url():
    return {'url': authentication.get_auth_url()}

@app.route("/home")
def home():
    if authentication.access_token is None:
        return redirect("/")
    return render_template('home.html')

@app.route("/design/list", methods=["GET"])
def designs():
    client = CanvaClient(auth=authentication)
    design_api = client.get_design_api()
    response = design_api.list_designs()
    return response.to_dict()

@app.route("/oauth/redirect", methods=['POST', 'GET'])
def oauth():
    code = request.args.get('code')
    state = request.args.get('state', default=None)
    print(f"Code: {code}\n State: {state}")
    authentication.get_access_token(code=code, state=state)
    return redirect('/home')
