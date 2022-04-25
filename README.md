# Dialogflow CX Speaker ID - Demo Ready
This repository is a practical demo-ready refactoring of Dialogflow Labs' Speaker ID proof-of-concept available to Googler's [internal only!] at https://cloud.google.com/dialogflow/priv/docs/labs/speaker-id

# Author(s)
- Fulfillment API: Yvan J. Aquino (yaquino@google.com)
- Dialogflow CX Agent: Anthony Okwechime (oktony@google.com)

# Goals
Dialogflow CX Speaker ID - Demo Ready was created to address the existing proof-of-concept's usability gaps while providing a cloud sales implementation that's customer demonstration ready.

The original Speaker ID proof-of-concept provides a DF CX agent and Cloud Functions based fulfillment that conveys the "gist" of Speaker ID usage; despite that, batteries are not included and some extra assembly is or may be required to adapt for customer-facing demonstrations.  

For example, the original proof-of-concept does not address "new user" journeys from within the experience but instead requires users to be staged into SQL  manually (out-of-band).  Resetting back to the original state also required the usage of direct SQL statements like those below:

```sql
TRUNCATE TABLE accounts CASCADE;
# OR
DELETE 
FROM    phones
# CREATE TABLE phones ... 
# FOREIGN KEY ... REFEFERENCES accounts (account_id) ON DELETE CASCADE
WHERE   phones.phone_number = ? 
```


# Significant Changes
## Critical User Journeys (CUJs)
The most significant "functional" changes come in the form of critical user journeys:

- As a first time user, I need to register an account.  My account will be looked up (transparently) by the caller_id parameter.

- As a first time user registering an account, I need to an provide alternate authentication in the form of a four digit pin.  If I provide this pin during account creation, the agent shouldn't  ask me for my pin in downstream flows and pages.

- As a first time user, if I successfully register an account, I will be re-directed to the existing Speaker ID Flow which detects existing Speaker IDs or asks me if I'd like to register a new one.

These critical user journey's address the CREATE AN ACCOUNT workflow we need for users to "stage" themselves into a Speaker ID demonstration via the agent.  

During the testing of Speaker ID - Demo Ready, the authors realized there was a need to constantly "reset" the database for agent functionality testing and, as such, new API route-methods (/delete-identity/{caller_id} and /gui/accounts) are provided to support the removal of user accounts from the database.

 - GET, DELETE /delete-identity/{caller_id}:  Accepts a 10 digit US phone number (IE: 6502530000) and then deletes all related accounts to the caller_id phone number.

 - GET /gui/accounts: Renders a simple HTML page that renders a table of accounts with phone numbers for easy deletion.  

These CUJs allow us to deliver a more cohesive demonstration by exposing more of the account lifecycle (which potentially aligns with realistic usage) and provide the demonstration maintainers with tools to remove / reset accounts without having to access the database directly.

## Platform
Dialogflow CX Speaker ID - Demo Ready uses Cloud Run instead of Cloud Functions for a number of reasons:

- Gen 1 Cloud Functions are 1 invocation to 1 call - This means that every single call will require the re-instantiation of clients resulting in added overhead and latency.  Cloud Run supports up to 80 concurrent calls at the same time by default, and up to 1000 simultaneous calls with the right configurations.  
  - with Cloud Run, we can define clients as part of the "global state" if and when it makes sense to do so - sessions and connections can be managed as necessary and can better leverage connection pooling should the demand scale upwards.     

- While it's possible to define ALL fulfillment webhooks routes and endpoints in a single Cloud Function, it's significantly cleaner and easier to use a web based framework to deliver webhook endpoints instead of using tags-based or some other variable based routing.  The "check-caller-id" page's fulfillment webhook's path is /check-caller-id; The "create-account" page routes to /create-account.
  - This also means that you're managing one "source" repo as opposed to multiple "sources" with Cloud Functions. 

- Creative liberty: With Cloud Run, services are defined in arbitrary Docker containers - granting the author the freedom to use whatever language / solution they choose!  Containers also serve as an beneficial abstraction on your application and facilitate portability and usage on other computing constructs (serverless ... or not!)

One of the great benefits of moving to Cloud Run is the freedom it affords the developer not only in language choice - but also  framework.  While the "de facto" framework for delivering web-based microservices is Flask; it's up to the  developer to decide what framework to use.

Dialogflow CX Speaker ID - Demo Ready was re-factored to FastAPI instead:

- FastAPI is natively asynchronous and runs on uvloop which is based off libuv - the very same loop that node.js uses.  FastAPI is just as fast as Node in most cases; in some cases it's as fast as Go's standard net/http library.  

- FastAPI has automatic document generation that's exposed on routes /docs and /redocs.  Very useful for troubleshooting!

- FastAPI relies on Pydantic, a data validation library that makes developing in Python look, feel, and behave like a statically-typed language.  While this may seem like a design compromise, it actually serves to the development experiences very, very similar to other languages like Go and C++ and keeps your data "on rails" and consistent.  

## Code Updates
There is nothing "wrong" with the code that https://cloud.google.com/dialogflow/priv/docs/labs/speaker-id provides.  In fact, the Speaker ID - Demo Ready implementation follows the spirit of the provided samples and accomplishes nearly the same things but does so in significantly different way.

1. The average definition for a web service route written in Cloud Functions is about 60 SLOC; the Speaker ID - Demo Ready version routes are just south of 20 SLOC.

2. Due to the nature of Cloud Functions, there is a good amount of "boiler plate" code that has to be repeated.  With Cloud Run, a lot of the boilerplate code can replaced with a decorator that allows for the composition of self-documenting code.  

```python
# Decorated version (8 SLOC, 11 including decorators + function def.)
@app.post("/verify-pin")
@staging
async def verify_pin(webhook: WebhookRequest, 
    response=..., caller_id=..., Session=..., session_id=..., pin=...):
    with Session() as session:
        account_ids = Phone.get_account_ids(session, caller_id)
        if not account_ids:
            # This should never happen in production 
            response.add_text_response(f"AccountError: No account was found for {caller_id}.")
            return response
        pins = Account.get_pins(session, account_ids)
        response.add_session_params({'userAuthenticated': pin in pins})
        return response

# Original version (18 SLOC, 20 including decorators + function def.)
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
```

3. Adoption and utilization of SQL Alchemy Object Relational Mapping.  While some languages, like Go, don't really benefit from an ORM, ORMS in Python can really shine.  SQL Alchemy is one of the most powerful ORMs out there so for Speaker ID - Demo Ready the decision was made to use SQL Alchemy as an ORM instead of just a connection broker.  

```python
# Without ORM
...
account_id = None
with db.connect() as conn:
    account_ids = conn.execute(
        "SELECT account_id FROM phone WHERE number = '{}'".format(caller_id).fetchall()
    )
for row in account_ids:
    account_id = row[0]
if not account_id:
    ...

# With ORM
...
    with Session() as session:
        account_ids = Phone.get_account_ids(session, caller_id)
        if not account_ids:
            ...
```

## Architecture
The original proof-of-concept demonstration recommends a trusted serverless applicaiton stack including Cloud Functions, Cloud SQL, and Dialogflow.  

Speaker ID - Demo Ready takes a more opinionated version of that route that aligns a bit better with security requirements in highly regulated markets like the Public Sector.  

- Cloud Run (Serverless computing, stateless, containers as a service)
- Cloud SQL (Postgres 14, Private Instance with no external IP, SSL/TLS 1.2)
- Serverless VPC Access Connector (to allow connectsion with Private SQL)
- Cloud Build (Serverless CI / CD)
- Secret Manager (Sensitive configuration and credentials management)
