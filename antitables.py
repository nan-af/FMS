from sqlalchemy import create_engine
from sqlalchemy.sql import text
from pathlib import Path


assert input("""ARE YOU EXTREMELY SURE THAT YOU WANT TO DELETE ALL TABLES?
Type "yes" to continue: """) == "yes"

engine = create_engine(Path("db_connection").read_text(), echo=True)
with engine.connect() as con:
    con.execute(text("""
    DROP TABLE if exists public.accounts CASCADE;

    DROP TABLE if exists public.attendance CASCADE;

    DROP TABLE if exists public.customer CASCADE;

    DROP TABLE if exists public.employee CASCADE;

    DROP TABLE if exists public.transactions CASCADE;

    DROP TABLE if exists public.vendor CASCADE;"""))
