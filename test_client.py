import requests

BASE_URL = 'http://127.0.0.1:5000/api'


def print_response(method, url, response):
    print('-' * 50)
    print(f'{method} {url}')
    print(f'Status: {response.status_code}')

    try:
        print(response.json())
    except ValueError:
        print(response.text)


# Создание пользователя
response = requests.post(
    f'{BASE_URL}/users',
    json={
        'first_name': 'Анна',
        'last_name': 'Иванова',
        'email': 'api_test@example.com',
        'password': '12345'
    }
)

print_response('POST', f'{BASE_URL}/users', response)

user_id = response.json().get('user_id')


# Получение пользователей
response = requests.get(f'{BASE_URL}/users')
print_response('GET', f'{BASE_URL}/users', response)


# Обновление пользователя
response = requests.put(
    f'{BASE_URL}/users/{user_id}',
    json={
        'first_name': 'Анна',
        'last_name': 'Петрова'
    }
)

print_response('PUT', f'{BASE_URL}/users/{user_id}', response)


# Создание новости
response = requests.post(
    f'{BASE_URL}/news',
    json={
        'title': 'Тестовая новость',
        'content': 'Новость создана через API.',
        'user_id': user_id
    }
)

print_response('POST', f'{BASE_URL}/news', response)

news_id = response.json().get('news_id')


# Получение новостей
response = requests.get(f'{BASE_URL}/news')
print_response('GET', f'{BASE_URL}/news', response)


# Обновление новости
response = requests.put(
    f'{BASE_URL}/news/{news_id}',
    json={
        'title': 'Обновлённая новость'
    }
)

print_response('PUT', f'{BASE_URL}/news/{news_id}', response)


# Удаление новости
response = requests.delete(
    f'{BASE_URL}/news/{news_id}'
)

print_response('DELETE', f'{BASE_URL}/news/{news_id}', response)


# Удаление пользователя
response = requests.delete(
    f'{BASE_URL}/users/{user_id}'
)

print_response('DELETE', f'{BASE_URL}/users/{user_id}', response)
