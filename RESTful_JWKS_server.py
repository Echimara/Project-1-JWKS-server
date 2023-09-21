# Name: Chimara Okeke
# Date: 9/19/2023
# Class: CSCE3550.001

# Usage: 
'''
---From Terminal---
1. pip install cryptography
'''    
# Description: 
 '''add later'''

import flask 
from flask import Flask, request
from flask import jsonify
import time
import os
import jwk
# key gen libs
import cryptography.hazmat
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

app = Flask(_name_) # create flask object

# KEY GENERATION - req1
# Generate an RSA key pair
private_key = rsa.generate_private_key(
    public_exponent=65537,  
    key_size=2048,          
    backend=default_backend()
)

# ASSOCIATE A KEY ID (KID) AND EXPIRY TIMESTAMP WITH EACH KEY - req2
key_id = "kid_1"
# Get time by epoch
curr_time = int(time.time())
#  expiry timestamp -: 2hrs
key_expiry = curr_time + 7200

# store keys
key_entry = {
    "key_id": key_id,
    "public_key": public_key,
    "key_expiry": key_expiry
}
keys = [key_entry]

# SERVE HTTP ON PORT 8080 - req3
if _name_ == '_main_':
    app.run(host='0.0.0.0', port=8080)


# RESTful JWKS endpoint - req4
@app.route('/jwks', methods=['GET'])
def jwks():
    current_time = int(time.time())
    if key_expiry <= current_time:
        key_expiry = current_time
    jwks = {
        "keys": [
            {
                "kid": key_id,
                "kty": "RSA",
                "alg": "RS256",
                "use": "sig",
                "n": public_key.public_numbers().n,
                "e": public_key.public_numbers().e,
                "exp": key_expiry,
            }
        ]
    }
    return jsonify(jwks)

# /auth endpoint definition with HTTP method - req5
@app.route('/auth', methods=['POST'])
def auth():
    # GET expired query parameter from the request
    expired_param = request.args.get('expired')

    # Parameter validation
    if expired_param:
        # If param is expired, generate a JWT using the expired key and expiry
        token = generate_jwt(private_key, key_id, expired=True)
    else:
        # generate a JWT using the current key and expiry
        token = generate_jwt(private_key, key_id)

 #  Return an unexpired, signed JWT on the POST request
 return jsonify({"access_token": token})

# /jwks endpoint to serve JWKS keys
@app.route('/jwks', methods=['GET'])
def jwks():
    current_time = int(time.time())
    jwks = {
        "keys": [
            {
                "kid": key_id,
                "kty": "RSA",
                "alg": "RS256",
                "use": "sig",
                "n": keys[key_id]["public_key"].n,
                "e": keys[key_id]["public_key"].e,
                "exp": keys[key_id]["key_expiry"],
            }
        ]
    }
    return jsonify(jwks)

# /auth endpoint to issue JWTs
@app.route('/auth', methods=['POST'])
def auth():
    expired_param = request.args.get('expired')
    token = generate_jwt(private_key, key_id, expired_param)

    return jsonify({"access_token": token})

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)




