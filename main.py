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
        select * from accounts"""))
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


# Case 5: view all customers DONE
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


# Case 8: view employee salary
@app.get("/salary")
async def salary(employee_id):
    with engine.begin() as con:
        salary = con.execute(text("""
        select hourly_wage from employee
        where employee_id = :emp_id
        """), emp_id=employee_id)
    return json2html.convert(json=list(salary))


# Case 9: view employee advance
@app.get("/advance")
async def advance(employee_id):
    with engine.begin() as con:
        advance = con.execute(text("""
        select amount from transaction, advance
        where advance.employee_id = :emp_id
        """), emp_id=employee_id)
    return json2html.convert(list(advance))


# Case 10: insert employee attendance
@app.post("/attendance")
async def attendance(employee_id=Form(...), date=Form(...), time_in=Form(...), time_out=Form(...), leave=Form(...), break_hours=Form(...)):
    with engine.begin() as con:
        attendance = con.execute(text("""
        INSERT INTO attendance VALUES
        (:employee_id, :date, :time_in, :time_out, :leave, :break_hours)
        """), employee_id=employee_id, date=date, time_in=time_in, time_out=time_out, leave=leave, break_hours=break_hours)
    return "Employee attendance updated"


# 11 View customer accounts easy, select * from accounts
@app.get("/customer_accounts")
async def customer_accounts():
    with engine.begin() as con:
        accounts = con.execute(text("""
        select * from accounts
        where account_id in (select account_id
                             from customer)
        """))  # , customers=getcustomers())
    return json2html.convert(list(accounts))


# # @app.get("/customers")
# async def getcustomers():
#     with engine.begin() as con:
#         customersList = con.execute(text("""
#         select id from customers
#         """))
#     return customersList


# 12 view stock easy, select * from stock
@app.get("/stock")
async def stock():
    with engine.begin() as con:
        stock = con.execute(text("""
        select * from stock """))
    return json2html.convert(list(stock))

# 13 view income DONE AS CASE 8
# 14 view leaves total - all taken leaves of an employee


@app.get("/attendance")
async def remainingLeaves(datefrom=Form(...), dateto=Form(...), employeeid=Form(...), total=Form(...)):
    with engine.begin() as con:
        leaves = con.execute(text("""
        select count(transaction_id) from attendance
        where employee_id = :employeeid and date_today between :datefrom and :dateto
         """), employeeid=employeeid, datefrom=datefrom, dateto=dateto)
    return str(total-leaves)+" remaining for employee with employee id {employeeid}."


# 15 add new item in inventory update stock
@app.post("/add_stock")
async def update_stock(quantity=Form(...), location=Form(...), total_weight=Form(...), rec_date=Form(...), use_date=Form(...), typ=Form(...)):
    with engine.begin() as con:
        tr = con.execute(text("""
        INSERT INTO stock VALUES
        (:quantity, :location, :total_weight, :rec_date, :use_date, :typ)
        """), quantity=quantity, location=location, total_weight=total_weight, rec_date=rec_date, use_date=use_date, typ=typ)
    return "Stock record updated"


# 16 remove item from stock
@app.post("/delete_stock")
async def remove_stock(stock_ID):
    with engine.begin() as con:
        delete_stock = con.execute(text("""
        	DELETE FROM stock
       		where stock.stock_ID = :stk_id
        """), stk_id=stock_ID)
    return "Stock deleted"


# 17 calculate employee wage income +/- overtime/undertime
@app.get("/wage")
async def wage(employee_id):
    with engine.begin() as con:
        wage = con.execute(text("""
        select hourly_wage from employee
        where employee_id = :emp_id
        """), emp_id=employee_id)
        time_put = con.execute(text("""
        select (time_out - time_in - break_hours) as time
        from attendance
        where employee_id = :emp_id
        """), emp_id=employee_id)
        calculated_wage = wage * time_put
    return calculated_wage


# 18 view orders select * from orders where status <> completed
@app.get("/orders")
async def orders():
    with engine.begin() as con:
        orders = con.execute(text("""
        select * from orders """))
    return json2html.convert(list(orders))


# 19 insert a transaction DONEE
@app.post("/transactions")
async def transaction(amount=Form(...), date=Form(...), from_account=Form(...), to_account=Form(...)):
    with engine.begin() as con:
        tr = con.execute(text("""
        INSERT INTO transactions (amount, tr_date, from_account, to_account)
        VALUES (:amount, :date, :from_account, :to_account)
        """), amount=amount, date=date, from_account=from_account, to_account=to_account)
    return "Transactions record updated"


# 20 view one customers account select * from account where id is
# @app.get("/accounts/{account_id}")
# async def customer_account(account_id):
#     with engine.begin() as con:
#         accounts = con.execute(text("""
#         select * from accounts
#         where id =:acc_id  """), acc_id=account_id)
#     return {"message": list(accounts)}


# 21 create new customer/vendor/employee DONEE
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
