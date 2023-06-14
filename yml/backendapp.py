import logging
import requests
from flask import Flask, request

app = Flask(__name__)

# Configure the logging settings
logging.basicConfig(filename='log.txt', level=logging.DEBUG)

@app.route('/', methods=['GET'])
def callback():
    code = request.args.get('code')
    print(f"Received code: {code}")  # Add this logging statement
    app.logger.debug(f"Received code: {code}")

    if code:
        # Code is present in the URL
        url = 'https://api-v2.upstox.com/login/authorization/token'
        headers = {
            'accept': 'application/json',
            'Api-Version': '2.0',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        data = {
            'code': code,
            'client_id': '11159d63-e478-4a53-b9e1-913eb80cc3f3',
            'client_secret': 'urstfzx1pu',
            'redirect_uri': 'https://upstoxapi.awsdinesh.xyz',
            'grant_type': 'authorization_code',
        }

        print("Sending POST request to", url)  # Add this logging statement
        print("Request data:", data)  # Add this logging statement

        app.logger.debug("Sending POST request to %s", url)
        app.logger.debug("Request data: %s", data)


        response = requests.post(url, headers=headers, data=data)

        print("Response status code:", response.status_code)  # Add this logging statement
        app.logger.debug("Response status code: %s", response.status_code)

        if response.status_code == 200:
            access_token = response.json()['access_token']
            return access_token
        else:
            raise Exception('Error getting access token: {}'.format(response.status_code))
    else:
        # Code is not present in the URL
        # Handle the situation accordingly
        return 'Authorization failed'



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082, debug=True)

