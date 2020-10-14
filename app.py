from flask import Flask, json, request, jsonify
import arc4, binascii, random, sys
from colorama import Fore, Style

cli = sys.modules['flask.cli']
cli.show_server_banner = lambda *x: None

api = Flask(__name__)

def encryptMe(someString):
    a = arc4.ARC4('This-is-an-encryption-key')
    cipherTextBin = a.encrypt(someString)
    return binascii.hexlify(cipherTextBin).decode()

def randMe(x):
    stringlets = "0987654321asdfghjkl"
    blob = ''.join(random.choice(stringlets) for _ in range(x))
    return blob

@api.route('/token', methods=['POST'])
def token():
    rBody = request.json
    # What we can use as a seed for token should never include the user credentials or identities
    # rAddr = request.remote_addr
    # rUserAgent = request.headers.get('User-Agent')
    username = rBody['Username']
    token = encryptMe(username)
    res = {"Token":token}
    res_json = json.dumps(res)
    response = jsonify(res_json)
    return response

@api.route('/whoami', methods=['POST'])
def whoami():
    rBody = request.json
    token = rBody['Token']
    if token == adminToken:
        res = {"Success":"You are logged in as admin"}
    else:
        res = {"Success":"You are logged in as an unprivileged user"}
    return jsonify(json.dumps(res))

if __name__ == '__main__':
    adminToken = encryptMe("admin")
    print("==> Generating \"admin\" token ... "+Fore.GREEN+adminToken+Style.RESET_ALL)
    print("==> Exposing REST api at http://127.0.0.1/token ...")
    print("==> Exposing REST api at http://127.0.0.1/whoami ...")
    api.run(host="0.0.0.0",port="80")