import requests
from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def callback():
    code = request.args.get('code')

    url = 'https://api-v2.upstox.com/login/authorization/token'
    headers = {
        'accept': 'application/json',
        'Api-Version': '2.0',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {
        'code': code,
        'client_id': 'e3fe3477-efac-4ff7-a0b9-3310a75d8fc8',
        'client_secret': 'wvzzsquu14',
        'redirect_uri': 'https://upstoxapi.awsdinesh.xyz',
        'grant_type': 'authorization_code',
    }

    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        access_token = response.json()['access_token']
        return access_token
    else:
        raise Exception('Error getting access token: {}'.format(response.status_code))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082, debug=True )
