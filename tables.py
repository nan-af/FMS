from sqlalchemy import create_engine
from sqlalchemy.sql import text

engine = create_engine("postgresql:///FMS", echo=True)
with engine.connect() as con:
    con.execute(text("""
    create table accounts(
        account_number serial primary key,
        opening_balance numeric
    )"""))

    con.execute(text("""
    create table transaction(
        tr_id serial primary key,
        amount numeric,
        tr_date date
    )"""))
