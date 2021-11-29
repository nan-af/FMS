from sqlalchemy import create_engine
from sqlalchemy.sql import text
from pathlib import Path


assert input("""ARE YOU EXTREMELY SURE THAT YOU WANT TO DELETE ALL TABLES?
Type "yes" to continue: """) == "yes"

engine = create_engine(Path("db_connection").read_text(), echo=True)
with engine.connect() as con:
    con.execute(text("""
    DROP TABLE IF EXISTS public.accounts CASCADE;

    DROP TABLE IF EXISTS public.advance CASCADE;

    DROP TABLE IF EXISTS public.allowance CASCADE;

    DROP TABLE IF EXISTS public.attendance CASCADE;

    DROP TABLE IF EXISTS public.customer CASCADE;

    DROP TABLE IF EXISTS public.employee CASCADE;

    DROP TABLE IF EXISTS public.orders CASCADE;

    DROP TABLE IF EXISTS public.purchased CASCADE;

    DROP TABLE IF EXISTS public.stock CASCADE;

    DROP TABLE IF EXISTS public.transactions CASCADE;

    DROP TABLE IF EXISTS public.vendor CASCADE;
    """))
