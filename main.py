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


# Case 4: view all employees
@app.get("/employees")
async def employees():
    with engine.connect() as con:
        employees = con.execute(text("""
        select * from employees"""))
    return {"message": list(employees)}


# Case 5: view all vendors
@app.get("/vendors")
async def vendors():
    with engine.connect() as con:
        vendors = con.execute(text("""
        select * from vendors"""))
    return {"message": list(vendors)}


# Case 5: view all customers
@app.get("/customers")
async def customers():
    with engine.connect() as con:
        customers = con.execute(text("""
        select * from customers"""))
    return {"message": list(customers)}


# Case 7: view employee Attendance
@app.get("/attendance")
async def attendance():
    with engine.connect() as con:
        attendance = con.execute(text("""
        select * from attendance"""))
    return {"message": list(attendance)}


# Case 8: view employee salary

# Case 9: view employee advance

# Case 10: insert employee attendance
