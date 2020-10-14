from flask import Flask, json, request, jsonify
import arc4, binascii, random, sys, time
from colorama import Fore, Style

# Remove Flask warning about production use
cli = sys.modules['flask.cli']
cli.show_server_banner = lambda *x: None

api = Flask(__name__)

# Create a token
def tokeniseMeNow(text):
    now = str(time.time())[:8]
    nowToken = encryptMe(text+now)
    return nowToken

# Simple RC4 encryption, no nonce.
def encryptMe(x):
    a = arc4.ARC4('This-is-an-encryption-key')
    cipherTextBin = a.encrypt(x)
    return binascii.hexlify(cipherTextBin).decode()

# Not in use, use if can attack in high volumes e.g. no rate limits
def randMe(x):
    stringlets = "0987654321asdfghjklzxcvbnmqwertyuiop"
    blob = ''.join(random.choice(stringlets) for _ in range(x))
    return blob

@api.route('/token', methods=['POST'])
def token():
    rBody = request.json
    # What we can use as a seed for token should never include the user credentials or identities
    # rAddr = request.remote_addr
    # rUserAgent = request.headers.get('User-Agent')
    username = rBody['Username']
    token = tokeniseMeNow(username)
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
    # create an encrypted token for the "admin" string and echo to terminal
    adminToken = tokeniseMeNow("admin")
    print("==> Generating \"admin\" token ... "+Fore.GREEN+adminToken+Style.RESET_ALL)
    print("==> Exposing REST api at http://127.0.0.1:5000/token ...")
    print("==> Exposing REST api at http://127.0.0.1:5000/whoami ...")
    api.run(host="0.0.0.0",port="5000")