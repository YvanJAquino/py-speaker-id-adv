# Dialogflow CX Speaker ID - Demo Ready
This repository is practical demo-ready refactoring of Dialogflow Labs' Speaker ID proof-of-concept available to Googler's [internal only!] at https://cloud.google.com/dialogflow/priv/docs/labs/speaker-id

# Author(s)
- Fulfillment API: Yvan J. Aquino (yaquino@google.com)
- Dialogflow CX Agent: Anthony Okwechime (oktony@google.com)

# Goals
Dialogflow CX Speaker ID - Demo Ready was created to address the existing proof-of-concept's usability gaps while providing a cloud sales 'reference' implementation that's customer demonstration ready.

The original Speaker ID proof-of-concept provides a functional agent and Cloud Functions based fulfillment designed to convey the "gist" of how Speaker ID works in a bubble - it is not  demonstration ready (nor was it meant to be) and requires a variety of tweaks to adapt for customer-facing demonstrations.  

For example, the original proof-of-concept did not address "new user" journeys from within the experience but instead requires users to be staged into SQL manually.  Resetting back to the original state also required the usage of direct SQL statements like those below:

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
## Critical User Journeys
The most significant "functional" changes come in the form of critical user journeys:

- As a first time user, I need to register an account.  My account will be looked up (transparently) by the caller_id parameter which has my phone number to confirm if I have an account or if I need to register an account.
- As a first time user registering an account, I need to provide alternate authentication in the form of a four digit pin.  If I provide this pin during account creation, the agent shouldn't need to ask me for my pin in downstream workflows.
- As a first time user, if I successfully register an account, I will be re-directed back to the existing Speaker ID Flow which detects for existing Speaker IDs or asks me if I'd like to register a new one.

These critical user journey's address the CREATE AN ACCOUNT workflow we need for users to "stage" themselves into a Speaker ID demonstration via the agent.  

During the testing of Speaker ID - Demo Ready, the authors realized there was a need to constantly "reset" the database for agent functionality testing and, as such, new API route-methods (/delete-identity/{caller_id} and /gui/accounts) are provided to support the removal of user accounts from the database.

 - GET, DELETE /delete-identity/{caller_id}:  Accepts a 10 digit US phone number (IE: 6502533000) and then deletes all related accounts to the caller_id phone number.

 - GET /gui/accounts: Renders a simple HTML page that renders a table of accounts with phone numbers for easy deletion.  

 