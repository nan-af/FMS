import requests
import random
import string


baseURL = 'http://127.0.0.1:8000'


def create_random_person():
    r = random.choice(('customer', 'vendor', 'employee'))
    n = random.choices(string.ascii_letters, k=5)
    a = random.choices(string.ascii_letters, k=15)
    p = random.choices(string.digits, k=12)
    o = random.randint(-100000, 100000)
    h = random.randint(50, 200) if r == 'employee' else 0

    return {'role': r, 'name': ''.join(n), 'address': ''.join(a), 'phone': ''.join(p), 'opening_balance': o, 'hourly_wage': h}


def create_random_transaction():
    r = requests.get(f'{baseURL}/accounts')
    ids = [a['account_id'] for a in r.json()]

    fa = random.choice(ids)
    while ((ta := random.choice(ids)) == fa):
        print('Collision!')
    print(fa, ta)

    amt = random.randint(-10000, 10000)

    t = {'amount': amt, 'date': '0000011111',
         'from_account': fa, 'to_account': ta}
    r = requests.post(f'{baseURL}/transactions', data=t)

    return r.text


for _ in range(100):
    p = create_random_person()
    r = requests.post(f'{baseURL}/create', data=p)

    print(r.text)

for _ in range(100):
    print(create_random_transaction())
