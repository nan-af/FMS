from sqlalchemy import create_engine
from sqlalchemy.sql import text
from pathlib import Path

engine = create_engine(Path("db_connection").read_text(), echo=True)
with engine.connect() as con:
    pass
