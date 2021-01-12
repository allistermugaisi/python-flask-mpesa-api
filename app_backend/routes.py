from flask import request
from app_backend import app
import requests 
from requests.auth import HTTPBasicAuth
import json
from datetime import datetime
import base64

# Mpesa credentials
consumer_key = "CONSUMER_KEY"
consumer_secret = "CONSUMER_SECRET"
base_url = "PUBLIC_IP_ADDRESS"

@app.route("/")
def home():
    return "Welcome to python-flask mpesa api"

# Get access token
@app.route("/access_token")
def token():

    data = _access_token()
    return data

# Register urls
@app.route("/register_urls")
def register():
    mpesa_endpoint = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"

    access_token = _access_token()

    headers = { "Authorization": "Bearer %s" % access_token }

    req_body = {
        "ShortCode": "",
        "ResponseType": "",
        "ConfirmationURL": base_url + '/c2b/confirmation',
        "ValidationURL": base_url + '/c2b/validation'
    }

    response = requests.post(mpesa_endpoint, json = req_body, headers = headers)
    return response.json()

  
@app.route('/c2b/validation', methods=['POST'])
def validate():
    # get data
    data = request.get_data()
    print(data)
    # accept transaction API call and respond to safaricom server
    return {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }



@app.route("/c2b/confirmation", methods=['POST'])
def confirm():
    # get data
    data = request.get_json()
    print(data)
    # accept transaction API call and respond to safaricom server
    return {
        "ResultCode":0,
        "ResultDesc":"Accepted"
    }


# Simulate C2B Transaction API
@app.route("/simulate")
def simulate():
    mpesa_endpoint = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/simulate"

    access_token = _access_token()

    headers = { "Authorization": "Bearer %s" % access_token }

    request_body = {
        "Amount": 100,
        "ShortCode": "",
        "BillRefNumber": "",
        "CommandID": "CustomerPayBillOnline",
        "Msisdn": ""
    }

    simulate_response = requests.post(mpesa_endpoint, json=request_body, headers=headers)

    return simulate_response.json()






# function to get access_token
def _access_token():
    
    mpesa_endpoint = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(mpesa_endpoint, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    data = r.json()
    return data['access_token']
