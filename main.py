from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.sql import text

app = FastAPI()
engine = create_engine("postgresql:///FMS", echo=True)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/accounts")
async def cust():
    with engine.connect() as con:
        accounts = con.execute(text("""
        select * from accounts"""))
    return {"message": list(accounts)}


@app.get("/transactions")
async def add_cust():
    with engine.connect() as con:
        transactions = con.execute(text("""
        select * from transactions"""))
    return {"message": list(transactions)}
