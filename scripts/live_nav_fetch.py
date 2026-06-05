import requests

print("LIVE NAV FETCH STARTED")

# placeholder API (you will replace later if Bluestock gives API)
url = "https://api.example.com/nav"

try:
    response = requests.get(url)
    print("API status:", response.status_code)
except Exception as e:
    print("Error:", e)