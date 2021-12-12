# from sqlalchemy import create_engine
# from sqlalchemy.sql import text
# from pathlib import Path

# engine = create_engine(Path("db_connection").read_text(), echo=True)
# with engine.connect() as con:
#     pass

import requests
import random
import string
from pprint import pprint


def create_random_person():
    r = random.choice(('customer', 'vendor', 'employee'))
    n = random.choices(string.ascii_letters, k=5)
    a = random.choices(string.ascii_letters, k=15)
    p = random.choices(string.digits, k=12)
    o = random.randint(1000, 100000)
    h = random.randint(50, 200) if r == 'employee' else None

    return {'role': r, 'name': ''.join(n), 'address': ''.join(a), 'phone': ''.join(p), 'opening_balance': o, 'hourly_wage': h}


for _ in range(100):
    p = create_random_person()
    r = requests.post('http://127.0.0.1:8000/create', data=p)

    # pprint(p)
    print(r.text)
    # print(str(p['name']))
