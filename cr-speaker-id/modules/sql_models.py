import uuid

import psycopg2
from sqlalchemy import Integer, Column, create_engine, ForeignKey, String, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


def guid():
    return str(uuid.uuid4())

Base = declarative_base()


class Account(Base):
    __tablename__ = 'accounts'
    account_id = Column(String, primary_key=True, default=guid)
    account_name = Column(String)
    account_pin = Column(String)

    @staticmethod
    def get_pins(session, account_ids):
        rows = list(
            session
                .query(Account.account_pin)
                .filter(Account.account_id.in_(account_ids))
        )
        return [row[0] for row in rows]

    @staticmethod
    def delete_account(session, account_id):
        account = (
            session
                .query(Account)
                .filter(Account.account_id==account_id)
                .one()
        )
        session.delete(account)
        session.commit()




class Phone(Base):
    __tablename__ = 'phones'
    phone_id = Column(String, primary_key=True, default=guid)
    account_id = Column(String, ForeignKey("accounts.account_id", ondelete='CASCADE'))
    phone_number = Column(String)

    @staticmethod
    def get_account_ids(session, phone_number):
        rows = list(
            session
                .query(Phone.account_id)
                .filter(Phone.phone_number == phone_number)
        )
        return [row[0] for row in rows]

    @staticmethod
    def delete_phone(session, phone_number):
        phone = (
            session
                .query(Phone)
                .filter(Phone.phone_number == phone_number)
                .first()
        )
        account_id = phone.account_id
        session.delete(phone)
        session.commit()
        return account_id
        
    @staticmethod
    def delete_identity(session, phone_number):
        phone = (
            session
                .query(Phone)
                .filter(Phone.phone_number == phone_number)
                .first()
        )
        account_id = phone.account_id
        session.delete(phone)
        session.commit()
        return account_id


class SpeakerId(Base):
    __tablename__ = 'speakerIds'
    speaker_id = Column(String, primary_key=True, default=guid)
    account_id = Column(String, ForeignKey("accounts.account_id", ondelete='CASCADE'))
    gcp_resource_name = Column(String)

    @staticmethod
    def get_speaker_ids(session, account_ids):
        rows = list(
            session
                .query(SpeakerId.gcp_resource_name)
                .filter(SpeakerId.account_id.in_(account_ids))
        )
        return [row[0] for row in rows]


def create_tables(engine):
    return Base.metadata.create_all(engine)
