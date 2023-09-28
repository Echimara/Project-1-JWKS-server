# Name: Chimara Okeke
# Date: 9/19/2023
# Class: CSCE3550.001

# Usage:
'''
---From Terminal---
1. pip install flask
2. pip install cryptography
3. pip install pyjwt
4. pip install rsa
5. pip install coverage
'''

# Description:
'''
This code implements a simple Flask application that generates RSA key pairs with unique IDs and expiry timestamps.
It provides a RESTful JWKS endpoint to serve public keys in JWKS format and an /auth endpoint to issue JWTs.
'''

import flask
from flask import Flask, request, jsonify
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import jwt
import time

# Create a Flask object
app = Flask(__name__)

# Key Generation - req1
# Generate multiple RSA key pairs with unique IDs and expiry timestamps
keys = {}
for i in range(3):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    public_key = private_key.public_key()
    key_id = f"kid_{i}"
    current_time = int(time.time())
    key_expiry = current_time + 7200
    keys[key_id] = {
        "private_key": private_key,
        "public_key": public_key,
        "key_expiry": key_expiry,
    }


# Generate JWT
def generate_jwt(private_key, key_id, expired=False):
    payload = {"sub": "userABC"} 

     # Set up signing key
    key = keys[key_id]["private_key"]

    
    if expired:
        key = keys[key_id]["private_key"]  # Use the expired key

    token = jwt.encode(payload, key, algorithm="RS256", headers={"kid": key_id})
    return token


# POST /auth - Generate and return a JWT
@app.route("/auth", methods=["POST"])
def auth():
    # Check if the "expired" query parameter is present
    expired_param = request.args.get("expired")

    # validation
    if expired_param:
        # If "expired" is present, generate a JWT using an expired key
        for key_id in keys:
            if keys[key_id]["key_expiry"] <= int(time.time()):
                token = generate_jwt(keys[key_id]["private_key"], key_id, expired=True)
                return jsonify({"access_token": token})

    # Generate a JWT using the current key
    for key_id in keys:
        if keys[key_id]["key_expiry"] > int(time.time()):
            token = generate_jwt(keys[key_id]["private_key"], key_id)
            return jsonify({"access_token": token})

    return jsonify({"message": "No valid keys available"}), 500


# RESTful JWKS endpoint - req2.2
@app.route("/auth/.well-known/jwks.json", methods=["GET"])
def get_jwks():
    current_time = int(time.time())
    jwks = {"keys": []}
    for key_id in keys:
        if keys[key_id]["key_expiry"] > current_time:
            jwks["keys"].append(
                {
                    "kid": key_id,
                    "kty": "RSA",
                    "alg": "RS256",
                    "use": "sig",
                    "n": keys[key_id]["public_key"].public_numbers().n,
                    "e": keys[key_id]["public_key"].public_numbers().e,
                }
            )
    return jsonify(jwks)   # Return an unexpired, signed JWT on the POST request


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

