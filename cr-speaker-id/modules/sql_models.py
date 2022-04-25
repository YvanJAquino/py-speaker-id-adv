# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import uuid

import psycopg2
from sqlalchemy import Integer, Column, create_engine, ForeignKey, String, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


def guid():
    """
    Client side UUID v4 Generator for SQLAlchemy
    """
    return str(uuid.uuid4())

Base = declarative_base()


class Account(Base):
    __tablename__ = 'accounts'
    account_id = Column(String, primary_key=True, default=guid)
    account_name = Column(String)
    account_pin = Column(String)

    def to_dict(self):
        return {
            "account_id": self.account_id,
            "account_name": self.account_name,
            "account_pin": self.account_pin
        }

    @staticmethod
    def check_account_id(session, account_id):
        ...

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
    account_id = Column(String, ForeignKey("accounts.account_id", ondelete='CASCADE')) # ondelete='CASCADE' - deletes related rows.
    phone_number = Column(String)

    def to_dict(self):
        return {
            "phone_id": self.phone_id,
            "account_id": self.account_id,
            "phone_number": self.phone_number
        }

    @staticmethod
    def check_caller_id(session, caller_id):
        caller_ids = list(
            session
                .query(Phone)
                .filter(Phone.phone_number == caller_id)
        )
        return bool(caller_ids)

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
    account_id = Column(String, ForeignKey("accounts.account_id", ondelete='CASCADE')) # ondelete='CASCADE' - deletes related rows.
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
