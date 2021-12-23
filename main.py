from pathlib import Path

from fastapi import FastAPI
from fastapi.param_functions import Form
from fastapi.responses import HTMLResponse
from json2html import *
from sqlalchemy import create_engine
from sqlalchemy.sql import text

app = FastAPI()
engine = create_engine(Path("db_connection").read_text(), echo=True)


@app.get("/")
async def root():
    return HTMLResponse(Path("frontend/index.html").read_text())


# Case 1: view all accounts DONE
@app.get("/accounts")
async def accounts():
    with engine.begin() as con:
        accounts = con.execute(text("""
        select * from accounts
        order by account_id"""))
    return json2html.convert(json=list(accounts))


# Case 2: view all transactions of a specific account DONE
@app.get("/account")
async def txns_for_account(account_id):
    print(account_id)
    with engine.begin() as con:
        txns = con.execute(text("""
        select * from transactions
        where from_account = :acc_id
        or to_account = :acc_id"""), acc_id=account_id)
    return json2html.convert(json=list(txns))


# Case 3: view all transactions DONE
@app.get("/transactions")
async def transactions():
    with engine.begin() as con:
        transactions = con.execute(text("""
        select * from transactions"""))
    return json2html.convert(json=list(transactions))


# Case 4: view all employees DONE
@app.get("/employees")
async def employees():
    with engine.begin() as con:
        employees = con.execute(text("""
        select * from employee"""))
    return json2html.convert(list(employees))


# Case 5: view all vendors DONE
@app.get("/vendors")
async def vendors():
    with engine.begin() as con:
        vendors = con.execute(text("""
        select * from vendor"""))
    return json2html.convert(list(vendors))


# Case 6: view all customers DONE
@app.get("/customers")
async def customers():
    with engine.begin() as con:
        customers = con.execute(text("""
        select * from customer"""))
    return json2html.convert(list(customers))


# Case 7: view employee Attendance DONE
@app.get("/attendance")
async def attendance():
    with engine.begin() as con:
        attendance = con.execute(text("""
        select * from attendance"""))
    return json2html.convert(list(attendance))

# Case 8: view employee hourly wage DONE
@app.get("/get_wage")
async def salary(employee_id):
    with engine.begin() as con:
        salary = con.execute(text("""
        select employee_id,name,hourly_wage from employee
        where employee_id = :emp_id
        """), emp_id=employee_id)
    return json2html.convert(json=list(salary))


# Case 9: get employee advance DONE
@app.get("/get_advance")
async def advance(employee_id):
    with engine.begin() as con:
        advance = con.execute(text("""
        select employee_id, amount, tr_date from transactions right outer join advance on transaction_id = tr_id
        where from_account = :emp_id
        """), emp_id=employee_id)
    return json2html.convert(list(advance))

# Case 10: insert employee attendance DONE
@app.post("/insert_attendance")
async def attendance(employee_id=Form(...), transaction_id=Form(...), date=Form(...), time_in=Form(...), time_out=Form(...), leave=Form(...), break_hours=Form(...)):
    # with engine.begin() as con:
        z = (time_out-time_in)
        # at = con.execute(text("""
        # INSERT INTO attendance (employee_id, transaction_id, at_date, time_in, time_out, leave, break_hours)
        # VALUES (:employee_id, :transaction_id, :date, :time_in, :time_out, :leave, :break_hours);
        # """), employee_id=employee_id, transaction_id=transaction_id, date=date, time_in=time_in, time_out=time_out, leave=leave, break_hours=break_hours)
    return z #"Attendance record updated"

# Case 11: add advance DONE
@app.post("/advance")
async def add_advance(employee_id=Form(...), amount=Form(...), date=Form(...)):
    with engine.begin() as con:
        con.execute(text('''
        with acc_id as (
            select account_id from employee
            where employee_id = :e_id
        )
        
        UPDATE accounts
        SET closing_balance = closing_balance - :amt
        WHERE account_id = (select * from acc_id);

        UPDATE accounts
        SET closing_balance = closing_balance + :amt
        WHERE account_id = 1;

        with tr_id as (
            with acc_id as (
                select account_id from employee
                where employee_id = :e_id
            )

            insert into transactions (amount, tr_date, from_account, to_account)
            values (:amt,
                    :date,
                    :e_id,
                    1)
            returning tr_id
        )
        insert into advance (transaction_id, employee_id)
        values ((select * from tr_id), :e_id)
        '''), e_id=employee_id, amt=amount, date=date)

    return "Advance updated"

# case 12: Get employee allowance DONE
@app.get("/allowance")
async def get_allowance_by_employee(employee_id):
    with engine.begin() as con:
        allowance_table = con.execute(text("""
        select type, employee_id, transaction_id, amount
        from allowance left outer join transactions on transaction_id = tr_id
        where employee_id = :e_id
        """), e_id = employee_id)
    return json2html.convert(json=list(allowance_table))

# case 13: Insert employee allowance DONE
@app.post('/allowance')
async def insert_employee_allowance(employee_id=Form(...), amount=Form(...), allowance_type=Form(...), date=Form(...)):
    with engine.begin() as con:
        con.execute(text('''
        with acc_id as (
            select account_id from employee
            where employee_id = :e_id
        )
        UPDATE accounts
        SET closing_balance = closing_balance - :amt
        WHERE account_id = (select * from acc_id);

        UPDATE accounts
        SET closing_balance = closing_balance + :amt
        WHERE account_id = 1;

        with tr_id as (
            with acc_id as (
                select account_id from employee
                where employee_id = :e_id
            )

            insert into transactions (amount, tr_date, from_account, to_account)
            values (:amt,
                    :date,
                    (select * from acc_id),
                    1)
            returning tr_id
        )
        insert into allowance (transaction_id, employee_id,type)
        values ((select * from tr_id), :e_id, :a_type)
        '''), e_id=employee_id, amt=amount, date=date,a_type = allowance_type)
        return "Allowances record updated successfully"    

# case 14: get employee attendance DONE
@app.get("/get_attendance")
async def get_attendance_by_employee(employee_id):
    print(employee_id)
    with engine.begin() as con:
        txns = con.execute(text("""
        select * from attendance
        where employee_id = :e_id
        """), e_id=employee_id)
    return json2html.convert(json=list(txns))

# case 15: view stock easy, select * from stock DONE
@app.get("/stock")
async def stock():
    with engine.begin() as con:
        stock = con.execute(text("""
        select * from stock """))
    return json2html.convert(list(stock))

# Case 16: View customer accounts easy, select * from accounts DONE
@app.get("/customer_accounts")
async def customer_accounts():
    with engine.begin() as con:
        accounts = con.execute(text("""
        select * from accounts
        where account_id in (select account_id
                             from customer)
        """))  # , customers=getcustomers())
    return json2html.convert(list(accounts))

# 17 add new item in inventory update stock DONE
@app.post("/add_stock")
async def update_stock( owner=Form(...), quantity=Form(...), location=Form(...), total_weight=Form(...), received_date=Form(...), use_date=Form(...), type=Form(...)):
    with engine.begin() as con:
        tr = con.execute(text("""
        INSERT INTO stock (owner, quantity, location, total_weight, received_date, use_date, type)
        VALUES (:owner, :quantity, :location, :total_weight, :received_date, :use_date, :type)
        """), owner=owner, quantity=quantity, location=location, total_weight=total_weight, received_date=received_date, use_date=use_date, type=type)
    return "Stock record updated"


# 18 remove item from stock DONE
@app.post("/delete_stock")
async def remove_stock(stock_ID=Form(...)):
    with engine.begin() as con:
        delete_stock = con.execute(text("""
        	DELETE FROM stock
       		where stock_ID = :stk_id
        """), stk_id=stock_ID)
    return "Stock deleted"

# 19 calculate employee wage income +/- overtime/undertime
@app.get("/wage")
async def wage(employee_id):
    with engine.begin() as con:
        wage = list(con.execute(text("""
        select hourly_wage from employee
        where employee_id = :emp_id
        """), emp_id=employee_id))
        wage = list(wage[0])
        time_put = list(con.execute(text("""
        select sum(time_out - time_in)
        from attendance
        where employee_id = :emp_id
        """), emp_id=employee_id))
        time_put = list(time_put[0])
        break_hours = list(con.execute(text("""
        select sum(break_hours)
        from attendance
        where employee_id = :emp_id
        """), emp_id=employee_id))
        break_hours = list(break_hours[0])
        break_hours = break_hours[0]
        difference = int(time_put[0].total_seconds())/3600
        difference -= int(break_hours)
        calculated_wage = int(wage[0]) * difference
    return calculated_wage

# 21 insert a transaction DONE
@app.post("/transactions")
async def transaction(amount=Form(...), date=Form(...), from_account=Form(...), to_account=Form(...)):
    with engine.begin() as con:
        tr = con.execute(text("""
        INSERT INTO transactions (amount, tr_date, from_account, to_account)
        VALUES (:amount, :date, :from_account, :to_account);

        UPDATE accounts
        SET closing_balance = closing_balance - :amount
        WHERE account_id = :from_account;

        UPDATE accounts
        SET closing_balance = closing_balance + :amount
        WHERE account_id = :to_account;
        """), amount=amount, date=date, from_account=from_account, to_account=to_account)
    return "Transactions record updated"


# 22 create new customer/vendor/employee DONE
@app.post("/create")
async def create(role=Form(...), name=Form(...), address=Form(...), phone=Form(...), opening_balance=Form(...), hourly_wage=Form(...)):
    print(hourly_wage)
    if role in {'customer', 'vendor', 'employee'}:
        with engine.begin() as con:
            id = con.execute(text(f'''
                with new_id as (
                    insert into accounts (opening_balance, closing_balance)
                    values (:ob, :ob)
                    returning account_id
                )
                insert into {role} (name, address, phone_number, account_id)
                values (:name, :address, :phone, (select * from new_id))
                returning account_id;
                '''), name=name, address=address, phone=phone, ob=opening_balance)

            id = id.first()[0]

            if role == 'employee':
                con.execute(text('''
                    update employee
                    set hourly_wage = :hw
                    where account_id = :id
                    '''), hw=hourly_wage, id=id)

        return f'Successfully created {role} {name} with account number {id}.'

    else:
        return {'error': 'Invalid type of person.'}

# 20 view orders select * from orders where status <> completed
@app.get("/orders")
async def orders():
    with engine.begin() as con:
        orders = con.execute(text("""
        select * from orders """))
    return json2html.convert(list(orders))

# Case 23: place an order
@app.post("/addOrder")
async def orders(customer_id=Form(...),vendor_id=Form(...), amount=Form(...), quantity=Form(...), item_name=Form(...), date=Form(...)):
    with engine.begin() as con:
        c_id_id = list(con.execute(text('''
            select account_id from customer
            where customer_id = :c_id
        '''), c_id = customer_id))
        c_id_id = list(c_id_id[0])
        c_id_id = int(c_id_id[0])

        v_id_id = list(con.execute(text('''
            select account_id from vendor
            where vendor_id = :v_id
        '''), v_id = vendor_id))
        v_id_id = list(v_id_id[0])
        v_id_id = int(v_id_id[0])
        con.execute(text('''
        UPDATE accounts
        SET closing_balance = closing_balance - :amt
        WHERE account_id = :c_id_id;

        UPDATE accounts
        SET closing_balance = closing_balance + :amt
        WHERE account_id = :v_id_id;

        with tr_id as (

            insert into transactions (amount, tr_date, from_account, to_account)
            values (:amt,
                    :date,
                    :c_id_id,
                    :v_id_id)
            returning tr_id
        )
            insert into orders (transaction_id, customer_id, quantity, item_name, due_date)
            values ((select * from tr_id), :c_id, :quantity, :item_name, :date )
        
        
        '''), c_id_id=c_id_id, v_id_id=v_id_id, c_id=customer_id, v_id=vendor_id, amt=amount, quantity=quantity, item_name=item_name, date=date)
    return "Order Added"

#Case 24: Get Account Details of One Vendor: 
@app.get("/one_vendor")
async def get_one_vendor(vendor_id):
    print(vendor_id)
    with engine.begin() as con:
        txns = con.execute(text("""
        with acc_id as(
            select account_id 
            from vendor
            where vendor_id = :a_id
        )
        
        select * from accounts
        where account_id = (select * from acc_id);
        """), a_id=vendor_id)
    return json2html.convert(json=list(txns))

#Case 25: Get Account Details of One Customer: 
@app.get("/one_customer")
async def get_one_customer(customer_id):
    print(customer_id)
    with engine.begin() as con:
        txns = con.execute(text("""
        with acc_id as(
            select account_id 
            from customer
            where customer_id = :a_id
        )
        
        select * from accounts
        where account_id = (select * from acc_id);
        """), a_id=customer_id)
    return json2html.convert(json=list(txns))

#Case 26: Get Account Details of One Employee: 
@app.get("/one_employee")
async def get_one_employee(employee_id):
    print(employee_id)
    with engine.begin() as con:
        txns = con.execute(text("""
        with acc_id as(
            select account_id 
            from employee
            where employee_id = :a_id
        )
        
        select * from accounts
        where account_id = (select * from acc_id);
        """), a_id=employee_id)
    return json2html.convert(json=list(txns))

# Case 27: view ALL employee advances DONE
@app.get("/all_advance")
async def all_advance_taken():
    with engine.begin() as con:
        adv = con.execute(text("""
        select * from advance"""))
    return json2html.convert(list(adv))

# Case 28: view ALL employee allowances DONE
@app.get("/all_allowance")
async def all_allow_taken():
    with engine.begin() as con:
        adv = con.execute(text("""
        select * from allowance"""))
    return json2html.convert(list(adv))