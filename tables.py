from sqlalchemy import create_engine
from sqlalchemy.sql import text

engine = create_engine("postgresql:///FMS", echo=True)
with engine.connect() as con:
    con.execute(text("""
    create table accounts(
        account_id serial primary key,
        opening_balance numeric
    )"""))

    con.execute(text("""
    create table transactions(
        tr_id serial primary key,
        amount numeric,
        tr_date date,
        from_account integer not null,
        to_account integer not null,

        foreign key(from_account, to_account)
        references accounts(account_id)
        on update cascade
    )"""))
