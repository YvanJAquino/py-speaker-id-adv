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
Dialogflow CX Speaker ID - Demo Ready uses Cloud Run instead of Cloud Functions.   