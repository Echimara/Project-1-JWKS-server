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
from flask import Flask, request, jsonify
import time
import rsa
import jwt

app = Flask(__name__)  # Create a Flask object

# Key Generation - req1
# Generate an RSA key pair
private_key, public_key = rsa.newkeys(2048)

# Associate a Key ID (KID) and expiry timestamp with each key - req2
key_id = "kid_1"
# Get time by epoch
curr_time = int(time.time())
# Expiry timestamp: 2 hours
key_expiry = curr_time + 7200

# Store keys
keys = {
    key_id: {
        "private_key": private_key,
        "public_key": public_key,
        "key_expiry": key_expiry
    }
}

# RESTful JWKS endpoint - req4
@app.route('/jwks', methods=['GET'])
def jwks():
    current_time = int(time.time())
    if keys[key_id]["key_expiry"] <= current_time:
        keys[key_id]["key_expiry"] = current_time

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

# JWT Generation - Include this function in your code
def generate_jwt(private_key, key_id, expired=False):
    payload = {"sub": "userABC"}  # Add more claims as needed

    # Set the key to be used for signing (expired or current)
    key = keys[key_id]["private_key"]
    
    if expired:
        key = expired_private_key  # Implement expired_private_key (if needed)
        
    token = jwt.encode(payload, key, algorithm="RS256")
    return token

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
        # Generate a JWT using the current key and expiry
        token = generate_jwt(private_key, key_id)

    # Return an unexpired, signed JWT on the POST request
    return jsonify({"access_token": token})

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)



