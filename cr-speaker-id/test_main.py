# from fastapi.testclient import TestClient
# from main import app

# client = TestClient(app)

import requests
import json

data = {
  "detectIntentResponseId": "879928b8-c41d-47b5-b8a0-95a89bb7ae2c",
  "intentInfo": {
    "lastMatchedIntent": "projects/oktony-cx/locations/global/agents/c8d8547e-389e-4a82-82e8-53d749a1eb64/intents/00000000-0000-0000-0000-000000000000",
    "displayName": "Default Welcome Intent",
    "confidence": 1.0
  },
  "pageInfo": {
    "currentPage": "projects/oktony-cx/locations/global/agents/c8d8547e-389e-4a82-82e8-53d749a1eb64/flows/00000000-0000-0000-0000-000000000000/pages/START_PAGE",
    "displayName": "Start Page"
  },
  "sessionInfo": {
    "session": "projects/oktony-cx/locations/global/agents/c8d8547e-389e-4a82-82e8-53d749a1eb64/environments/-/sessions/0652w_75YFCR9671PWkrBnTZA"
  },
  "fulfillmentInfo": {
    "tag": "testing-webhook"
  },
  "messages": [{
    "text": {
      "text": ["Welcome..."],
      "redactedText": ["Welcome..."]
    },
    "responseType": "HANDLER_PROMPT",
    "source": "VIRTUAL_AGENT"
  }],
  "payload": {
    "telephony": {
      "caller_id": "+12123815659"
    }
  },
  "triggerIntent": "projects/oktony-cx/locations/global/agents/c8d8547e-389e-4a82-82e8-53d749a1eb64/intents/00000000-0000-0000-0000-000000000000",
  "languageCode": "en-US"
}

def test_read_main():
    url = 'https://py-speaker-id-adv-p47xccvrva-uc.a.run.app/check-caller-id'
    response = requests.post(url, json=data)
    print(json.dumps(response.json(), indent=2))

test_read_main()