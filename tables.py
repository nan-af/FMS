from sqlalchemy import create_engine
from sqlalchemy.sql import text
from pathlib import Path

engine = create_engine(Path("db_connection").read_text(), echo=True)
with engine.connect() as con:

    # updates closing_balance
    # con.execute(text("""
    # create trigger update_account
    #     after Insert
    #     on transactions
    #     Begin
    #         update table account
    #         set accounts.closing_balance = accounts.closing_balance + new.amount
    #         where account_id = new.from_account

    #         update table account
    #         set accounts.closing_balance = accounts.closing_balance - new.amount
    #         where account_id = new.to_account
    #     End
    # )"""))

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

        foreign key(from_account)
        references accounts(account_id)
        on update cascade,
        foreign key(to_account)
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
        account_id integer not null,

        foreign key(account_id)
        references accounts(account_id)
        on update cascade
    )"""))

    # creates VENDOR table
    con.execute(text("""
    create table vendor(
        vendor_id serial primary key,
        name char,
        address varchar(30),
        phone_number varchar(15),
        account_id integer not null,

        foreign key(account_id)
        references accounts(account_id)
        on update cascade
    )"""))

    # creates CUSTOMER table
    con.execute(text("""
    create table customer(
        customer_id serial primary key,
        name char,
        address varchar(30),
        phone_number varchar(15),
        account_id integer not null,

        foreign key(account_id)
        references accounts(account_id)
        on update cascade
    )"""))

    # creates ATTENDANCE table
    con.execute(text("""
    create table attendance(
        employee_id integer not null,
        transaction_id integer primary key,
        time_in time not null,
        time_out time not null,
        leave boolean,
        break_hours int,

        foreign key(employee_id)
        references employee(employee_id)
        on update cascade,

        foreign key(transaction_id)
        references transactions(tr_id)
        on update cascade
    )"""))

    # creates STOCK table
    con.execute(text("""
    create table stock(
        stock_id serial primary key,
        owner integer,
        quantity int,
        location varchar(30),
        total_weight numeric,
        received_date date,
        use_date date,
        type varchar(30),

        foreign key(owner)
        references customer(customer_id)
        on update cascade
    )"""))

    # creates PURCHASED FROM table
    con.execute(text("""
    create table purchased(
        stock_id integer not null,
        vendor_id integer not null,
        transaction_id integer not null,

        PRIMARY KEY(stock_id, vendor_id, transaction_id),

        foreign key(stock_id)
        references stock(stock_id)
        on update cascade,

        foreign key(vendor_id)
        references vendor(vendor_id)
        on update cascade,

        foreign key(transaction_id)
        references transactions(tr_id)
        on update cascade
    )"""))

    # creates ALLOWANCE table
    con.execute(text("""
    create table allowance(
        type varchar(30),
        employee_id integer not null,
        transaction_id integer not null primary key,

        foreign key(transaction_id)
        references transactions(tr_id)
        on update cascade,

        foreign key(employee_id)
        references employee(employee_id)
        on update cascade
    )"""))

    # # creates UTILISED table
    # con.execute(text("""
    # create table utilised(
    #     employee_id integer not null,
    #     transaction_id integer not null,
    #     PRIMARY KEY(employee_id, transaction_id)
    # )"""))

    # creates E_AT table
    # con.execute(text("""
    # create table e_at(
    #     date_today date,
    #     employee_id integer not null,
    #     transaction_id integer not null,
    #     PRIMARY KEY(date_today, employee_id, transaction_id)
    # )"""))

    # creates ADVANCE table
    con.execute(text("""
    create table advance(
        transaction_id integer not null primary key,
        employee_id integer not null,

        foreign key(transaction_id) 
        references transactions(tr_id)
        on update cascade,

        foreign key(employee_id) 
        references employee(employee_id)
        on update cascade
    )"""))

    # creates ORDER table
    con.execute(text("""
    create table orders(
        order_id serial primary key,
        transaction_id integer not null,
        customer_id integer not null,
        quantity integer,
        item_name varchar(15),
        due_date date,

        foreign key(transaction_id) 
        references transactions(tr_id)
        on update cascade,

        foreign key(customer_id) 
        references customer(customer_id)
        on update cascade
    )"""))

    # creates WILL_USE table
    con.execute(text("""
    create table will_use(
        order_id integer not null,
        stock_id integer not null,

        primary key(order_id, stock_id),

        foreign key(order_id)
        references orders(order_id)
        on update cascade,

        foreign key(stock_id)
        references stock(stock_id)
        on update cascade
    )"""))
