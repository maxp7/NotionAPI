import requests
import os
from dotenv import load_dotenv
load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
RESERVIERUNGEN_DB = os.getenv("RESERVIERUNGEN_DB")
AUSLEIHE_DB = os.getenv("AUSLEIHE_DB")
knownPageIds = set()
fetchedResults ={}

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
    global fetchedResults
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
        fetchedResults = results
    return results


def checkNewEntries():
    global knownPageIds

    results = paginate_notion_db(RESERVIERUNGEN_DB)
    currentIds = {page['id'] for page in results}
    
    allFieldsOk = True  
    
    for page in fetchedResults:
        try:
            name = page["properties"]["Name"]["title"][0]["plain_text"]
            if not name:
                print("Please choose the name")
                allFieldsOk = False
        except (KeyError, IndexError, TypeError):
            print("Please choose the name")
            allFieldsOk = False

        try:
            deviceName = page["properties"]["Gerätname"]["formula"]["string"]
            if not deviceName:
                print("Please choose the device")
                allFieldsOk = False
        except (KeyError, TypeError):
            print("Please choose the device")
            allFieldsOk = False

        try:
            formel = page["properties"]["Formel"]["formula"]["string"]
        except (KeyError, TypeError):
            allFieldsOk = False

        try:
            start_date = page["properties"]["Startdatum"]["date"]["start"]
            if not start_date:
                print("Please choose the start date")
                allFieldsOk = False
        except (KeyError, TypeError):
            print("Please choose the start date")
            allFieldsOk = False

        try:
            end_date = page["properties"]["Enddatum"]["date"]["start"]
            if not end_date:
                print("Please choose the end date")
                allFieldsOk = False
        except (KeyError, TypeError):
            print("Please choose the end date")
            allFieldsOk = False

    if currentIds != knownPageIds and allFieldsOk:
        knownPageIds = currentIds
        return True  
    
    return False
