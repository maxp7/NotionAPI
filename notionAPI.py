import requests
import os
from dotenv import load_dotenv
load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
RESERVIERUNGEN_DB = os.getenv("RESERVIERUNGEN_DB")
AUSLEIHE_DB = os.getenv("AUSLEIHE_DB")
lastUpdateTime = 0

# Request headers
HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

def paginate_notion_db(database_id):
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    results = []
    has_more = True
    next_cursor = None

    while has_more:
        payload = {"start_cursor": next_cursor} if next_cursor else {}
        response = requests.post(url, headers=HEADERS, json=payload)
        if response.status_code != 200:
            print(f"Failed to fetch entries: {response.status_code}, {response.text}")
            break
        data = response.json()
        results.extend(data.get("results", []))
        has_more = data.get("has_more", False)
        next_cursor = data.get("next_cursor")

    return results

def checkNewEntries():
    global lastUpdateTime 
    results = paginate_notion_db(RESERVIERUNGEN_DB)
    for page in results:
        currentUpdateTime = page['last_edited_time']
        if(currentUpdateTime == lastUpdateTime):
            return False
           
    lastUpdateTime = currentUpdateTime
    return True
