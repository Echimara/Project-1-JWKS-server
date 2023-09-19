# Name: Chimara Okeke
# Date: 9/19/2023
# Class: CSCE3550.001

# Usage: 
# Description: 

# Needed libs
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

# Key Generation - req1
# Generate an RSA key pair
private_key = rsa.generate_private_key(
    public_exponent=65537,  
    key_size=2048,          
    backend=default_backend()
)

# Associate a Key ID (kid) and expiry timestamp with each key.
key_id = "kid_1"
