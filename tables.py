from sqlalchemy import create_engine
from sqlalchemy.sql import text
from pathlib import Path

engine = create_engine(Path("db_connection").read_text(), echo=True)
with engine.connect() as con:

    # updates closing_balance
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

    # creates ACCOUNTS table
    con.execute(text("""
    create table accounts(
        account_id serial primary key,
        opening_balance numeric,
        closing_balance numeric
    )"""))

    # creates TRANSACTIONS table
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

    # creates EMPLOYEE table
    con.execute(text("""
    create table employee(
        employee_id serial primary key,
        name char,
        address varchar(30),
        phone_number varchar(15),
        hourly_wage numeric,
        account_id serial
    )"""))

    # creates VENDOR table
    con.execute(text("""
    create table vendor(
        vendor_id serial primary key,
        name char,
        address varchar(30),
        phone_number varchar(15),
        account_id serial
    )"""))

    # creates CUSTOMER table
    con.execute(text("""
    create table customer(
        customer_id serial primary key,
        name char,
        address varchar(30),
        phone_number varchar(15),
        account_id serial
    )"""))

    # creates ATTENDANCE table
    con.execute(text("""
    create table attendance(
        date_today date primary key,
        employee_id serial,
        time_in time not null,
        time_out time not null,
        leave ,
        break_hours int 

        foreign key(employee_id)
        references accounts(employee)
        on update cascade
    )"""))
