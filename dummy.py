import requests
import random
import string
import html_to_json
import datetime


baseURL = 'http://127.0.0.1:8000'


def get_account_ids() -> list[int]:
    return [a['account_id'] for a in html_to_json.convert_tables(requests.get(f'{baseURL}/accounts').text)[0]]


def random_date():
    start_date = datetime.date(2000, 1, 1)
    end_date = datetime.date(2021, 12, 31)
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)

    return random_date


def create_random_person():
    r = random.choice(('customer', 'vendor', 'employee'))
    n = random.choices(string.ascii_letters, k=5)
    a = random.choices(string.ascii_letters, k=15)
    p = random.choices(string.digits, k=12)
    o = random.randint(-100000, 100000)
    h = random.randint(50, 200) if r == 'employee' else 0

    return {'role': r, 'name': ''.join(n), 'address': ''.join(a), 'phone': ''.join(p), 'opening_balance': o, 'hourly_wage': h}


def create_random_transaction():
    ids = get_account_ids()

    fa = random.choice(ids)
    while ((ta := random.choice(ids)) == fa):
        print('Collision!')
    print(fa, ta)

    amt = random.randint(-10000, 10000)

    t = {'amount': amt, 'date': random_date(),
         'from_account': fa, 'to_account': ta}
    r = requests.post(f'{baseURL}/transactions', data=t)

    return r.text


def create_random_advance():
    r = requests.get(f'{baseURL}/employees')
    ids = [e['employee_id'] for e in html_to_json.convert_tables(r.text)[0]]

    amt = random.randint(1, 1000)

    a = {'employee_id': random.choice(
        ids), 'amount': amt, 'date': random_date()}
    r = requests.post(f'{baseURL}/advance', data=a)

    return r.text


for _ in range(input("Enter number of persons to create:")):
    p = create_random_person()
    r = requests.post(f'{baseURL}/create', data=p)

    print(r.text)

for _ in range(input('Enter number of transactions to create:')):
    print(create_random_transaction())

for _ in range(input('Enter number of advance records to create:')):
    print(create_random_advance())
