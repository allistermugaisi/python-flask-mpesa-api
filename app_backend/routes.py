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
        "ResponseType": "Complete",
        "ConfirmationURL": base_url + '/c2b/confirmation',
        "ValidationURL": base_url + '/c2b/validation'
    }

    response = requests.post(mpesa_endpoint, json = req_body, headers = headers)
    return response.json()

# Callback URLS for validation and confimation 

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
        "BillRefNumber": "TestAPI",
        "CommandID": "CustomerPayBillOnline",
        "Msisdn": ""
    }

    simulate_response = requests.post(mpesa_endpoint, json=request_body, headers=headers)

    return simulate_response.json()


# Simulate Lipa na M-Pesa Online Payment Transaction API
@app.route("/lnmo")
def init_stk():
    mpesa_endpoint = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

    access_token = _access_token()

    headers = { "Authorization": "Bearer %s" % access_token }
    

    my_endpoint = base_url + "/lnmo"

    Timestamp = datetime.now()

    times = Timestamp.strftime("%Y%m%d%H%M%S")

    password = "BUSINESS_SHORT_CODE" + "PASS_KEY" + times

    encoded_pass = base64.b64encode(password.encode("utf-8"))

    data = {
        "BusinessShortCode": "",
        "Password": encoded_pass,
        "Timestamp": times,
        "TransactionType": "CustomerPayBillOnline",
        "PartyA": "", # fill with your phone number
        "PartyB": "",
        "PhoneNumber": "", # fill with your phone number
        "CallBackURL": my_endpoint,
        "AccountReference": "TestPay",
        "TransactionDesc": "Lipa na Mpesa Online Simulation",
        "Amount": 2
    }

    res = requests.post(mpesa_endpoint, json = data, headers = headers)
    return res.json()

# Callback URL for Lipa na Mpesa Online
@app.route("/lnmo", methods=["POST"])
def lnmo_result():
    data = request.get_data()
    print(data)


# Simulate B2C Transaction API
@app.route("/b2c")
def make_payment():

    mpesa_endpoint = "https://sandbox.safaricom.co.ke/mpesa/b2c/v1/paymentrequest"

    access_token = _access_token

    headers = { "Authorization": "Bearer %s" % access_token }

    my_endpoint = base_url + "/b2c"

    data = {
        "InitiatorName": "apitest342",
        "SecurityCredential": "GENERATE_KEY",
        "Amount": "200",
        "PartyA": "",
        "PartyB": "254708374149",
        "Remarks": "Pay Salary",
        "QueueTimeOutURL": my_endpoint + "/timeout",
        "ResultURL": my_endpoint + "/result",
        "Occasion": "Salary"
    }

    res = requests.post(mpesa_endpoint, json = data, headers = headers)
    return res.json()

# Callback URLS for result and timeout

@app.route("/b2c/result", methods=["POST"])
def result_b2c():
    data = request.get_data()
    print(data)


@app.route("/b2c/timeout", methods=["POST"])
def b2c_timeout():
    data = request.get_json()
    print(data)


# function to get access_token
def _access_token():
    
    mpesa_endpoint = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(mpesa_endpoint, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    data = r.json()
    return data['access_token']
