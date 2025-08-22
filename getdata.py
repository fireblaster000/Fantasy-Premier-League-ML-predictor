import requests
import json
##doesnt work because sofascore blocked api requests apparently, couldn't find a way to bypass

# Step 1: Start a session (keeps cookies automatically)
session = requests.Session()

# Step 2: Visit Sofascore homepage to get cookies
session.get("https://www.sofascore.com", headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/115.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9"
})

# Step 3: Now call the API with the same session (cookies included)
api_url = "https://www.sofascore.com/api/v1/event/14038670/lineups"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/115.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.sofascore.com/",
    "Origin": "https://www.sofascore.com"
}

response = session.get(api_url, headers=headers)

# Step 4: Print nicely
try:
    data = response.json()
    print(json.dumps(data, indent=2))
except json.JSONDecodeError:
    print("Raw response:", response.text)
