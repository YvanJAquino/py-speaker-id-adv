from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modules.sql_models import Account, Phone, SpeakerId


DB_USER = "speakeridsys"
DB_PASS = "speakeridsys"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "postgres"
DB_CNST = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

print(DB_CNST)

engine = create_engine(DB_CNST)
Session = sessionmaker(engine)

s = '+17862511624'
print(s[2:])

with Session() as session:
    acct_x = Account(account_name="testing", account_pin="0326")
    session.add(acct_x)
    session.commit()
    phone_x = Phone(account_id=acct_x.account_id, phone_number="+17862511624")
    session.add(phone_x)
    session.commit()

with Session() as session:
    accounts = session.query(Account).all()
    for account in accounts:
        print(account.to_dict())

# with Session() as session:
#     phones = [
#         phone.to_dict()
#         for phone in session.query(Phone).all()
#     ]
#     print(phones)
#     for phone in phones:
#         Account.delete_account(session, phone['account_id'])