import re
import os
import string

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI, HTTPException

from modules.models import WebhookRequest
from modules.whr_client import WebhookResponse
from modules.sql_models import Account, Phone, SpeakerId

# Reserved for database configuration
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_NAME = os.environ.get("DB_NAME")
# DB_CNST = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
DB_CNST = os.environ.get("DB_CNST") 

# Database engine and session objects
engine = create_engine(DB_CNST)
Session = sessionmaker(engine)

phone_regex = re.compile('\+1\d{10}$')

app = FastAPI()

@app.post("/default")
async def default(webhook: WebhookRequest):
    response = WebhookResponse()
    phone = webhook.payload['telephony']['caller_id']
    msg = "We found you in our records. "
    response.add_text_response(msg)
    response = response.to_dict()
    session_params = {'sessionInfo': {
                'parameters': {
                    'caller_id': phone
                    }
                }
            }
    response.update(session_params)
    return response

@app.post("/check-caller-id")
async def check_caller_id(webhook: WebhookRequest):
    response = WebhookResponse()
    phone = webhook.payload['telephony']['caller_id']
    with Session() as session:
        account_ids = Phone.get_account_ids(session, phone)
    if not account_ids:
        response.add_text_response("No account was found!")
        response.add_session_params({"phonenum_exists": False})
    else:
        response.add_text_response("account was found!")
        response.add_session_params({"phonenum_exists": True})

    return response.to_dict()

@app.post("/create-account")
async def create_account(webhook: WebhookRequest):
    response = WebhookResponse()
    phone = webhook.payload['telephony']['caller_id']
    pin = webhook.sessionInfo.parameters.get("pin")
    with Session() as session:
        account_ids = Phone.get_account_ids(session, phone)
        if not account_ids:
            new_acct = Account(account_name="testing", account_pin=pin)
            session.add(new_acct)
            session.commit() # added in case necessary.
            new_phone = Phone(account_id=new_acct.account_id, phone_number=phone)
            session.add(new_phone)
            session.commit()
            response.add_text_response("An account was created for you.")
            response.add_session_params({"newaccount_created": True})
        else:
            # This should never happen
            response.add_text_response("I found an account but something went wrong.  Check the logs!")
    return response.to_dict()

@app.post("/get-speaker-ids")
async def get_speaker_ids(webhook: WebhookRequest):
    response = WebhookResponse()
    phone = webhook.payload['telephony']['caller_id']
    with Session() as session:
        account_ids = Phone.get_account_ids(session, phone)
        if not account_ids:
            # This should not happen anymore.
            response.add_text_response(f"No account was found for: {phone}.")
            return response.to_dict()
        speaker_ids = SpeakerId.get_speaker_ids(session, account_ids)
        if not speaker_ids:
            response.add_text_response("No speaker IDs were found for this phone number.")
            return response.to_dict()
        else:
            response.add_text_response("Speaker IDs found!  Let's move on...")
            response = response.to_dict()
            session_params = {'sessionInfo': {
                'parameters': {
                    'speaker-ids': speaker_ids
                    }
                }
            }
            response.update(session_params)
            return response

@app.post("/register-speaker-ids")
async def register_speaker_ids(webhook: WebhookRequest):
    response = WebhookResponse()
    phone = webhook.payload['telephony']['caller_id']
    new_speaker_id = webhook.sessionInfo.parameters['new-speaker-id']
    with Session() as session:
        account_ids = Phone.get_account_ids(session, phone)
        if not account_ids:
            # this should NEVER happen
            response.add_text_response(f"AccountError: No account was found for {phone}.")
            return response.to_dict()
        account_id = account_ids[0]
        session.add(SpeakerId(gcp_resource_name=new_speaker_id, account_id=account_id))
        session.commit()
        response.add_text_response("A new speaker ID has been registered.")
        response = response.to_dict()
        session_params = {'sessionInfo': {
            'parameters': {
                'speakerIdRegistered': True,
                'userAuthenticated': True
                }
            }
        }
        response.update(session_params)
        return response

@app.post("/verify-pin")
async def verify_pin(webhook: WebhookRequest):
    response = WebhookResponse()
    phone = webhook.payload['telephony']['caller_id']
    pin = webhook.pageInfo['formInfo']['parameterInfo'][0]['value']
    with Session() as session:
        account_ids = Phone.get_account_ids(session, phone)
        if not account_ids:
            response.add_text_response(f"AccountError: No account was found for {phone}.")
            return response.to_dict()
        pins = Account.get_pins(session, account_ids)
        response.add_text_response("Verifying by pin... you are now authenticated!")
        response = response.to_dict()
        session_params = {'sessionInfo': {
            'parameters': {
                'userAuthenticated': pin in pins
                }
            }
        }
        response.update(session_params)
        return response

@app.delete("/delete-identity/{caller_id}", status_code=204)
async def delete_identity(caller_id: str):
    if not (len(caller_id) and caller_id.isdigit()):
        raise HTTPException(status_code=404, detail=f"Phone {caller_id} was not deleted")
    else:
        caller_id = "+1" + caller_id
    
    with Session() as session:
        account_id = Phone.delete_phone(session, phone_number=caller_id)
        Account.delete_account(session, account_id)

