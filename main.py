from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from pathlib import Path

app = FastAPI()
engine = create_engine(Path("db_connection").read_text(), echo=True)


@app.get("/")
async def root():
    return HTMLResponse(Path("frontend/index.html").read_text())


# Case 1: view all accounts
@app.get("/accounts")
async def accounts():
    with engine.connect() as con:
        accounts = con.execute(text("""
        select * from accounts"""))
    return {"message": list(accounts)}


# Case 2: view all transactions of a specific account
@app.get("/account/{account_id}")
async def txns_for_account(account_id):
    with engine.connect() as con:
        txns = con.execute(text("""
        select * from transactions
        where from_account = :acc_id
        or to_account = :acc_id"""), acc_id=account_id)
    return {"message": list(txns)}


# Case 3: view all transactions
@app.get("/transactions")
async def transactions():
    with engine.connect() as con:
        transactions = con.execute(text("""
        select * from transactions"""))
    return {"message": list(transactions)}


<<<<<<< HEAD
#Case 4: view all employees
=======
# Case 4: view all employees
>>>>>>> origin/master
@app.get("/employees")
async def employees():
    with engine.connect() as con:
        employees = con.execute(text("""
        select * from employees"""))
    return {"message": list(employees)}


<<<<<<< HEAD
#Case 5: view all vendors
=======
# Case 5: view all vendors
>>>>>>> origin/master
@app.get("/vendors")
async def vendors():
    with engine.connect() as con:
        vendors = con.execute(text("""
        select * from vendors"""))
    return {"message": list(vendors)}


<<<<<<< HEAD
#Case 5: view all customers
=======
# Case 5: view all customers
>>>>>>> origin/master
@app.get("/customers")
async def customers():
    with engine.connect() as con:
        customers = con.execute(text("""
        select * from customers"""))
    return {"message": list(customers)}


<<<<<<< HEAD
=======
# Case 7: view employee Attendance
@app.get("/attendance")
async def attendance():
    with engine.connect() as con:
        attendance = con.execute(text("""
        select * from attendance"""))
    return {"message": list(attendance)}


# Case 8: view employee salary
@app.get("/salary/{employee_id}")
async def salary(employee_id):
    with engine.connect() as con:
        salary = con.execute(text("""
        select hourly_wage from employee
        where employee_id = :emp_id
        """), emp_id=employee_id)
    return {"message": list(salary)}


# Case 9: view employee advance
@app.get("/advance/{employee_id}")
async def advance(employee_id):
    with engine.connect() as con:
        advance = con.execute(text("""
        select amount from transaction, advance
        where advance.employee_id = :emp_id
        """), emp_id=employee_id)
    return {"message": list(advance)}


# Case 10: insert employee attendance
@app.post("/attendance")
async def attendance(employee_id, date, time_in, time_out, leave, break_hours):
    with engine.connect() as con:
        attendance = con.execute(text("""
        INSERT INTO attendance VALUES
        (:employee_id, :date, :time_in, :time_out, :leave, :break_hours)
        """), employee_id=employee_id, date=date, time_in=time_in, time_out=time_out, leave=leave, break_hours=break_hours)
    return {"message": "Employee attendance updated"}

# 11 View customer accounts easy, select * from accounts 
@app.get("/accounts")
async def customer_accounts():
    with engine.connect() as con:
        accounts = con.execute(text("""
        select * from accounts
        where id in ( select id from customer)
        """))
    return {"message": list(accounts)}
# 12 view stock easy, select * from stock
@app.get("/stock")
async def stock():
    with engine.connect() as con:
        stock = con.execute(text("""
        select * from stock """))
    return {"message": list(stock)}
# 13 view income
# 14 view leaves total - all taken leaves of an employee
# 15 add new item in inventory update stock
@app.post("/stock")
async def update_stock(quentity, location,total_weight, rec_date, use_date,typ):
    with engine.connect() as con:
        tr = con.execute(text("""
        INSERT INTO stock VALUES
        (:quentity, :location, :total_weight, :rec_date, :use_date, :typ)
        """), quentity=quentity, location=location,total_weight=total_weight, rec_date=rec_date, use_date=use_date,typ=typ)
    return {"message": "Stock record updated"}
# 16 remove item from inventory 
# 17 calculate employee wage income +/- overtime/undertime
# 18 view orders select * from orders where status <> completed
@app.get("/orders")
async def orders():
    with engine.connect() as con:
        orders = con.execute(text("""
        select * from orders """))
    return {"message": list(orders)}
# 19 input transaction insert a transaction 
@app.post("/transactions")
async def transaction(amount, date, from_account, to_account,):
    with engine.connect() as con:
        tr = con.execute(text("""
        INSERT INTO transactions VALUES
        (:amount, :date, :from_account, :to_account)
        """), amount=amount, date=date, from_account=from_account, to_account=to_account)
    return {"message": "Transactions record updated"}
# 20 view one customers account select * from account where id is 
@app.get("/accounts/{account_id}")
async def customer_account(account_id):
    with engine.connect() as con:
        accounts = con.execute(text("""
        select * from accounts
        where id =:acc_id  """),acc_id = account_id)
    return {"message": list(accounts)}
>>>>>>> origin/master
