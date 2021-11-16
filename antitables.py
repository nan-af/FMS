from sqlalchemy import create_engine
from sqlalchemy.sql import text

assert input("""ARE YOU EXTREMELY SURE THAT YOU WANT TO DELETE ALL TABLES?
Type "yes" to continue: """) == "yes"

engine = create_engine("postgresql:///FMS", echo=True)
with engine.connect() as con:
    con.execute(text("""
    drop table *"""))
