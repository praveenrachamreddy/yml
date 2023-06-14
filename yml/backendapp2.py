import logging
import subprocess
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
        # Proceed with exchanging the code for an access token
        # Make the necessary cURL request to Upstox API to obtain the access token

        curl_command = (
            "curl -X POST 'https://api-v2.upstox.com/login/authorization/token' "
            "-H 'accept: application/json' "
            "-H 'Api-Version: 2.0' "
            "-H 'Content-Type: application/x-www-form-urlencoded' "
            "-d 'code={}&client_id=11159d63-e478-4a53-b9e1-913eb80cc3f3&client_secret=urstfzx1pu&redirect_uri=https://upstoxapi.awsdinesh.xyz&grant_type=authorization_code'"
        ).format(code)

        response = subprocess.run(curl_command, shell=True, capture_output=True, text=True)

        print("Response status code:", response.returncode)  # Add this logging statement
        app.logger.debug("Response status code: %s", response.returncode)

        if response.returncode == 0:
            access_token = response.stdout  # Extract the access token from the response
            return access_token
        else:
            raise Exception('Error getting access token: {}'.format(response.stderr))
    else:
        # Code is not present in the URL
        # Handle the situation accordingly
        return 'Authorization failed'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082, debug=True)
