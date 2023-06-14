import requests
import csv
import logging


# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Define the NSE API endpoint for Nifty50
url = "https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%2050"

# Define request headers
headers = {
    "Accept-Encoding": "gzip",
    "Accept-Language": "en-US,en;q=0.9,hi;q=0.8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
}

# Define cookies
cookies = {
    "bm_sv": "B82C5273FCCDD71F9DBF32E58608024B~YAAQBNcLF9py2QaIAQAA076gGBOoAkR+AdNv4l1hkihsKEaPplzkQPDF+Eu8Tev5EDEOl3ot56kitlkZXpu20GvkzVAKvDcrPXxTzGSkYplBy9uKLd5Usru+i2S8hXINxsbOq6cNc2v/LGWjfvtbF2IEBVxwe1PDrETPVM0dTLXRgnaX72I1ZkUBz+xC2shZR1ofsRRYXGSO3shRkxDK/0IaC4Hqay0BohwOvVlS9wM5PtfW5AaHLMUDjqty/+U50Wpk~1"
}

# Log the request details
logging.debug(f"Sending GET request to URL: {url}")
logging.debug(f"Request Headers: {headers}")
logging.debug(f"Request Cookies: {cookies}")

# Send the GET request to the NSE API with headers and cookies
response = requests.get(url, headers=headers, cookies=cookies)

# Log the response details
logging.debug(f"Response Status Code: {response.status_code}")
logging.debug(f"Response Content: {response.content}")


# Check if the request was successful
if response.status_code == 200:
    print(response.content.decode())  # Add this line to print the response content
    # Parse the JSON response
    data = response.json()
    
    # Extract Nifty50 stock data
    nifty50_data = data["data"]

    # Save the Nifty50 stock data to a CSV file
    with open("nifty50_data.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Symbol", "Open", "High", "Low", "Last Price", "Change", "Percentage Change"])
        
        for stock in nifty50_data:
            writer.writerow([
                stock["symbol"],
                stock["open"],
                stock["dayHigh"],
                stock["dayLow"],
                stock["lastPrice"],
                stock["change"],
                stock["pChange"]
            ])

    logging.info("Nifty50 data saved to nifty50_data.csv")

    print("Nifty50 data saved successfully!")

else:
    print("Failed to fetch Nifty50 data. Error:", response.status_code)
    logging.error(f"Failed to fetch Nifty50 data. Error: {response.status_code}")
