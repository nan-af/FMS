from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from pathlib import Path

app = FastAPI()
engine = create_engine(Path("db_connection").read_text(), echo=True)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/accounts")
async def accounts():
    with engine.connect() as con:
        accounts = con.execute(text("""
        select * from accounts"""))
    return {"message": list(accounts)}


@app.get("/account/{account_id}")
async def txns_for_account(account_id):
    with engine.connect() as con:
        txns = con.execute(text("""
        select * from transactions
        where from_account = :acc_id
        or to_account = :acc_id"""), acc_id=account_id)
    return {"message": list(txns)}


@app.get("/transactions")
async def transactions():
    with engine.connect() as con:
        transactions = con.execute(text("""
        select * from transactions"""))
    return {"message": list(transactions)}
