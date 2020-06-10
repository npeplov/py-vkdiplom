import json
import time
from pprint import pprint

import requests
import sys


TOKEN = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'
params = {
    'access_token': TOKEN,
    'v': 5.89
}


# Получить инфо о группе по айди
def get_group_info_by_id(group_id):
    params['group_id'] = group_id
    loc_response = requests.get('https://api.vk.com/method/groups.getById', params)

    # Получаем значения name, gid и members_count из response:
    gid = group_id
    name = loc_response.json()['response'][0]['name']
    members_count = loc_response.json()['response'][0]['members_count']

    # В словарь  group записывам ключи name, gid, members_count
    group_dict = {'name': name, 'gid': gid, 'members_count': members_count}
    return group_dict


# Получить список id друзей:
def get_friends_id_list():
    params['user_id'] = user_id
    loc_response = requests.get('https://api.vk.com/method/friends.get', params)
    # print(loc_response.json())
    return loc_response.json()['response']['items']


"""""
Входные данные:
Имя пользователя или его id в ВК, для которого мы проводим исследование.
Внимание: и имя пользователя (eshmargunov) и id (171691064) 
являются валидными входными данными.

eshmargunov входные данные
по алиасу получить id

account.getProfileInfo
screen_name

"""
# 1 Получаем id
# 1.1 Из переменной
user_id = 171691064

# 1.2 Из cmd
if len(sys.argv) < 2:
    # 1.3 Из input
    # try:
    #     print('Нажмите Enter, чтобы использовать 171691064')
    #     user_id = int(input("Введите id пользователя: "))
    # except ValueError:
    user_id = 'eshmargunov'
else:
    user_id = sys.argv[1]


# Если user_id - строка:
if isinstance(user_id, str):
    params['user_ids'] = user_id
    response = requests.get('https://api.vk.com/method/users.get', params)
    user_id = response.json()['response'][0]['id']
    print(user_id)


# 1.3 Функция возвращает список id друзей
friends_list = get_friends_id_list()


friend_groups = []
# 2. Получаем список id групп пользователя
params['user_id'] = user_id
response = requests.get('https://api.vk.com/method/groups.get', params)
user_groups_ids = response.json()['response']['items']


# 3. цикл по списку друзей:
for friend_id in friends_list:
    # 4. Получаем список групп каждого друга по очереди
    params['user_id'] = friend_id
    time.sleep(0.2)
    response = requests.get('https://api.vk.com/method/groups.get', params)
    # print(response.json())
    print('*', end='')
    if 'error' not in response.json():
        friend_groups = response.json()['response']['items']
    # 5. Сравнить c со списком групп юзера
    for user_gr_id in user_groups_ids:
        if user_gr_id in friend_groups:
            user_groups_ids.remove(user_gr_id)


# 6. Получаем дополнительное поле - "Число участников группы", с помощью параметра запроса
params['fields'] = 'members_count'
groups_list = []

# 7. Идем циклом по списку id групп
for gr_id in user_groups_ids:
    groups_list.append(get_group_info_by_id(gr_id))
    time.sleep(0.5)

# 8. Запись списка групп в файл
with open('groups.json', 'w', encoding="utf-8") as fo:
    json.dump(groups_list, fo, ensure_ascii=False)

