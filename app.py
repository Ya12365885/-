from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, this is your application running!"

@app.route('/register', methods=['POST'])
def register_msisdn():
    url = "https://apim.djezzy.dz/oauth2/registration"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "*/*",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 6.0; LG-X230 Build/MRA58K)",
        "Host": "apim.djezzy.dz",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip"
    }
    msisdn = request.json.get('msisdn')
    msisdn = '213' + msisdn[1:]  # remove the first digit and add 213 at the beginning

    data = {
        "scope": "smsotp",
        "client_id": "6E6CwTkp8H1CyQxraPmcEJPQ7xka",
        "msisdn": msisdn
    }

    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        return jsonify({"Client ID": data["client_id"]}), 200
    except requests.exceptions.RequestException as err:
        return jsonify({"error": str(err)}), 400

@app.route('/token', methods=['POST'])
def get_auth_token():
    url = "https://apim.djezzy.dz/oauth2/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "*/*",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 6.0; LG-X230 Build/MRA58K)",
        "Host": "apim.djezzy.dz",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip"
    }
    otp = request.json.get('otp')
    data = {
        "scope": "openid",
        "client_secret": "MVpXHW_ImuMsxKIwrJpoVVMHjRsa",
        "client_id": "6E6CwTkp8H1CyQxraPmcEJPQ7xka",
        "otp": otp,
        "mobileNumber": "213782135601",
        "grant_type": "mobile"
    }

    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        return jsonify(response.json()), 200
    except requests.exceptions.RequestException as err:
        return jsonify({"error": str(err)}), 400

@app.route('/customer_care', methods=['POST'])
def send_customer_care_request():
    url = "https://apim.djezzy.dz/djezzy-api/cc/services/v1/customer_care/213782135601"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer 2ac02d8f-1f3f-3101-936b-ed5355e33cfa",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 6.0; LG-X230 Build/MRA58K)",
        "Host": "apim.djezzy.dz",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip"
    }
    bNumber = request.json.get('bNumber')
    data = {
        "type": "bipsms",
        "data": {
            "Subscriber": {
                "msisdn": "21382135601",
                "SubscriberTypeId": "MIXTEPREPAID"
            },
            "Option": {
                "id": 1,
                "bNumber": bNumber,
                "channel": 2
            }
        }
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        return jsonify(response.json()), 200
    except requests.exceptions.RequestException as err:
        return jsonify({"error": str(err)}), 400

if __name__ == '__main__':
    app.run(debug=True)
