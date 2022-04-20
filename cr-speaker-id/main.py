import json
import os
import string

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

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

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def staging(path_fn):
    """
    staging replaces boilerplate tasks (creating a response instance, 
    a database session, extracting the caller_id, and the session_id)
    with a decorator 
    
    Keyword Arguments
    -----------------
    response : WebhookResponse
        an WebhookResponse instance for responding.
    caller_id: str
        the phone number of the caller.
    Session: sqlalchemy.orm.Session
        A new sessionmaker instance (based off the engine definition).
        Session is capitalized to represent it's initializer has not 
        been called.
    session_id: str
        The WebhookRequests's session ID.
    pin: str
        The account's associated pin (if provided, else None)
    """
    async def call(webhook: WebhookRequest, 
        response=None, caller_id=None, Session=None, session_id=None, pin=None):
        response = WebhookResponse()
        caller_id = webhook.payload['telephony']['caller_id']
        Session = sessionmaker(engine)
        session_id = webhook.sessionInfo.session
        pin = None if not webhook.sessionInfo.parameters else webhook.sessionInfo.parameters.get("pin")
        return await path_fn(webhook, 
            response=response, caller_id=caller_id, 
            Session=Session, session_id=session_id, pin=pin)
    return call

@app.post("/default")
@staging
async def default(webhook: WebhookRequest, 
    response=..., caller_id=..., Session=..., session_id=..., pin=...):
    response.add_text_response("We found you in our records. ")
    response.add_session_params({'session': session_id, 'caller_id': caller_id})
    return response

@app.post("/check-caller-id")
@staging
async def check_caller_id(webhook: WebhookRequest, 
    response=..., caller_id=..., Session=..., session_id=..., pin=...):
    with Session() as session:
        account_ids = Phone.get_account_ids(session, caller_id)
    if not account_ids:
        response.add_text_response("No account was found!")
        response.add_session_params({"phonenum_exists": False})
    else:
        response.add_text_response("account was found!")
        response.add_session_params({"phonenum_exists": True})

    return response

@app.post("/create-account")
@staging
async def create_account(webhook: WebhookRequest, 
    response=..., caller_id=..., Session=..., session_id=..., pin=...):
    with Session() as session:
        account_ids = Phone.get_account_ids(session, caller_id)
        if not account_ids:
            new_acct = Account(account_name="testing", account_pin=pin)
            session.add(new_acct)
            session.commit() # added in case necessary.
            new_phone = Phone(account_id=new_acct.account_id, phone_number=caller_id)
            session.add(new_phone)
            session.commit()
            response.add_text_response("An account was created for you. ")
            response.add_session_params({"newaccount_created": True})
        else:
            # This should never happen
            response.add_text_response("I found an account but something went wrong.  Check the logs!")
    return response

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
        # response.add_text_response(" ... you are now authenticated!")
        response = response.to_dict()
        session_params = {'sessionInfo': {
            'parameters': {
                'userAuthenticated': pin in pins
                }
            }
        }
        response.update(session_params)
        return response

def _delete_identity(caller_id: str):
    result = {}
    if not (len(caller_id) == 10 and caller_id.isdigit()):
        result.update({"status": "COULD_NOT_DELETE", "caller_id": caller_id})
        print(json.dumps(result))
        raise HTTPException(status_code=404, detail=f"Phone {caller_id} was not deleted")
    else:
        result.update({"status": "SUCCESSFULLY_DELETED", "caller_id": caller_id})
        print(json.dumps(result))
    
    caller_id = "+1" + caller_id
    
    with Session() as session:
        account_ids = Phone.get_account_ids(session, caller_id)
        for account_id in account_ids:
            Account.delete_account(session, account_id)

    return result

@app.get("/delete-identity/{caller_id}", status_code=204)
async def get_delete_identity(caller_id: str):
    return _delete_identity(caller_id)

@app.delete("/delete-identity/{caller_id}", status_code=204)
async def delete_identity(caller_id: str):
    return _delete_identity(caller_id)



@app.get("/gui/accounts", response_class=HTMLResponse)
async def gui_accounts(request: Request):
    with Session() as session:

        phones = [
            phone.to_dict()
            for phone in session.query(Phone).all()
        ]
        print(phones)
        for phone in phones:
            caller_id = phone['phone_number'][2:]
            url = f'https://py-speaker-id-adv-p47xccvrva-uc.a.run.app/delete-identity/{caller_id}'
            phone.update({"delete_url": url})

        print(phones)

        template_values = {
            "columns": ["phone_id", "account_id", "phone_number"], 
            "values": phones,
            "request": request
        }
        # Test this!

    return templates.TemplateResponse("accounts.html", template_values)



# @app.post("/create-account")
# async def create_account(webhook: WebhookRequest):
#     response = WebhookResponse()
#     phone = webhook.payload['telephony']['caller_id']
#     pin = webhook.sessionInfo.parameters.get("pin")
#     with Session() as session:
#         account_ids = Phone.get_account_ids(session, phone)
#         if not account_ids:
#             new_acct = Account(account_name="testing", account_pin=pin)
#             session.add(new_acct)
#             session.commit() # added in case necessary.
#             new_phone = Phone(account_id=new_acct.account_id, phone_number=phone)
#             session.add(new_phone)
#             session.commit()
#             response.add_text_response("An account was created for you. ")
#             response.add_session_params({"newaccount_created": True})
#         else:
#             # This should never happen
#             response.add_text_response("I found an account but something went wrong.  Check the logs!")
#     return response.to_dict()
