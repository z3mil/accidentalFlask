[![MIT License][license-shield]][license-url]

# accidentalFlask
A Ssimple vulnerable Python API for educational purposes, specifically built for token entropy abuse. The app is built in Python 3 with Flask and exposes 2 APIs at "/token" and "/whomai".

#### Clone and install dependencies
``` 
git clone https://github.com/threatact0r/accidentalFlask.git 
cd accidentalFlask
python3 -m pip install -r requirement.txt
```

#### Run 
``` python3 app.py & ```

![running the app][product-screenshot]

#### Exploit
On every run, the ```admin``` token is generated and echoed to terminal. The ```token``` endpoint will create a weak RC4 encrypted blob based on the provided username, students can use tools like attack proxies (e.g. Burp sequencer) to enumrate the entropy of the token, and attempt to generate a valid ```admin``` token. An admin token can be verified by hitting the ```whoami``` endpoint which will respond with ```You are logged in as admin``` if the token matches. RC4 is vulnerable to bit-flipping, this can be done with Burp intruder or any other automation tool.

1. token endpoint
``` 
curl --location --request POST 'http://127.0.0.1:5000/token' \
--header 'Content-Type: application/json' \
--data-raw '{
    "Username": "bdmin",
    "Password": "password"
}'
```
2. whoami endpoint
```
curl --location --request POST 'http://127.0.0.1:5000/whoami' \
--header 'Content-Type: application/json' \
--data-raw '{
    "Token": "<insert_token_here>"
}'
```
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=flat-square
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[product-screenshot]: images/product-screenshot.png
