# Test with pytest -s for std-out messages

import os
import json
import uuid
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from modules.models import WebhookRequest, SessionInfo
from modules.whr_client import WebhookResponse
from modules.sql_models import Phone

from main import app

DB_CNST = os.environ.get("DB_CNST") 
engine = create_engine(DB_CNST)

client = TestClient(app)

def test_check_caller_id_1():
    caller_id = "+12123815659"
    request = WebhookRequest(
        detectIntentResponseId=str(uuid.uuid4()),
        languageCode="en-US",
        payload={"telephony": {"caller_id": caller_id}},
        pageInfo={},
        sessionInfo=SessionInfo(session=str(uuid.uuid4()))
    )
    response = client.post("/check-caller-id", json=request.dict(exclude_none=True))
    result = WebhookResponse(**response.json())
    phonenum_exists = result.sessionInfo.parameters.get('phonenum_exists')
    
    with sessionmaker(engine)() as session:
        assert phonenum_exists == Phone.check_caller_id(session, caller_id)

def test_check_caller_id_2():
    caller_id = "+17862511624"
    request = WebhookRequest(
        detectIntentResponseId=str(uuid.uuid4()),
        languageCode="en-US",
        payload={"telephony": {"caller_id": caller_id}},
        pageInfo={},
        sessionInfo=SessionInfo(session=str(uuid.uuid4()))
    )
    response = client.post("/check-caller-id", json=request.dict(exclude_none=True))
    result = WebhookResponse(**response.json())
    phonenum_exists = result.sessionInfo.parameters.get('phonenum_exists')    
    with sessionmaker(engine)() as session:
        assert phonenum_exists == Phone.check_caller_id(session, caller_id)
    
def test_create_account(delete=True):
    caller_id = "+17862511624"
    request = WebhookRequest(
        detectIntentResponseId=str(uuid.uuid4()),
        languageCode="en-US",
        payload={"telephony": {"caller_id": caller_id}},
        pageInfo={'formInfo': {'parameterInfo': [{'value': '1234'}]}},
        sessionInfo=SessionInfo(session=str(uuid.uuid4()))
    )
    response = client.post("/create-account", json=request.dict(exclude_none=True))
    result = WebhookResponse(**response.json())
    newaccount_created = result.sessionInfo.parameters.get('newaccount_created')
    with sessionmaker(engine)() as session:
        account_ids = Phone.get_account_ids(session, caller_id)
        assert newaccount_created == bool(account_ids)
    if delete:
        response = client.delete(f'/delete-identity/{caller_id[2:]}')
        assert response.status_code == 204


    