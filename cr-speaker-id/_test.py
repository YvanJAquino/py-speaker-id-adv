from modules.sql_models import Account, Phone, SpeakerId
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "postgres"
DB_USER = "speakeridsys"
DB_PASS = "sys"

DB_CNST = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DB_CNST, pool_pre_ping=True)
Session = sessionmaker(engine)


with Session() as session:
    # # Create an account
    # yvan = Account(account_name="test-1", account_pin="0149")
    # session.add(yvan)
    # session.commit()
    # yvans_phone = Phone(account_id=yvan.account_id, phone_number="+17862511624")
    # session.add(yvans_phone)
    # session.commit()

    # # Delete the accounts and phone numbers
    # acct_id = Phone.delete_phone(session, "+17862511624")
    # print(acct_id)
    # Account.delete_account(session, acct_id)


    