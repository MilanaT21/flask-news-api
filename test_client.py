import requests

BASE = 'http://127.0.0.1:5000/api'

response = requests.post(f'{BASE}/users', json={
    'first_name': 'Анна',
    'last_name': 'Иванова',
    'email': 'anna2@mail.ru',
    'password': '12345'
})
print(response.json())

response = requests.get(f'{BASE}/users')
print(response.json())

response = requests.post(f'{BASE}/news', json={
    'title': 'Первая новость',
    'content': 'Содержимое новости',
    'user_id': 1
})
print(response.json())

response = requests.get(f'{BASE}/news')
print(response.json())
