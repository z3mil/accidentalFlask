[![MIT License][license-shield]][license-url]

<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/threatact0r/accidentalFlask">
    <img src="images/logo.png" alt="Logo" width="100" height="100">
  </a>

  <h3 align="center">accidentalFlask</h3>

  <p align="center">
    A simple vulnerable token machine
    <br />
  </p>
</p>

# LOL, What is this?
A simple vulnerable Python API for educational purposes, specifically built for token entropy / bad session management abuse. The app is built in Python 3 with Flask and exposes 2 APIs at ```/token``` and ```/whomai```. The web app runs locally and does not incorporate any backend storage.

#### Clone and install dependencies
``` 
git clone https://github.com/z3mil/accidentalFlask.git
cd accidentalFlask
python3 -m pip install -r requirement.txt
```

#### Run 
``` python3 app.py & ```

![running the app][screenshot1]

#### Exploit Manually
On every run, the ```admin``` token is generated and echoed to terminal. The ```token``` endpoint will create a weak RC4 encrypted blob based on the provided username and a substring of current epoch time, students can use tools like attack proxies (e.g. Burp sequencer) to enumrate the entropy of the token, and attempt to generate a valid ```admin``` token. An admin token can be verified by hitting the ```whoami``` endpoint which will respond with ```You are logged in as admin``` if the token matches. RC4 is a stream cipher that is known to be vulnerable to bit-flipping.

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
#### Automate
The attack set out to achieve a valid admin token can be done with Burp intruder or any other automation tool. A generated token for a similar user (e.g. 'bdmin') will generate a close enough cipher text to be bit-flipped. the ```whoami``` endpoint will return a different response if an admin token is presented.

![Burp Intruder][screenshot2]

[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=flat-square
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[screenshot1]: images/screenshot1.png
[screenshot2]: images/screenshot2.png
