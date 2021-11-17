from sqlalchemy import create_engine
from sqlalchemy.sql import text
from pathlib import Path

engine = create_engine(Path("db_connection").read_text(), echo=True)
with engine.connect() as con:

	#updates closing_balance
	con.execute(text("""
	create trigger update_account
		after Insert
		on transactions
		Begin
			update table account
			set accounts.closing_balance = accounts.closing_balance + new.amount
			where account_id = new.from_account

			update table account
			set accounts.closing_balance = accounts.closing_balance - new.amount
			where account_id = new.to_account
		End	
    )"""))

	#creates ACCOUNTS table
    con.execute(text("""
    create table accounts(
        account_id serial primary key,
        opening_balance numeric,
        closing_balance numeric
    )"""))


    #creates TRANSACTIONS table
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
