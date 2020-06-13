import json
import time
import requests
import sys

# В константу TOKEN введите токен
TOKEN = ''
params = {
    'access_token': TOKEN,
    'v': 5.89
}


# 1 Получаем id
# 1.1 Из переменной
user_vk_id = 171691064


def get_input_data():
    # 1.2 Из cmd
    if len(sys.argv) < 2:
        # 1.3 Из input
        try:
            print('Нажмите Enter, чтобы использовать 171691064')
            loc_user_id = int(input("Введите id пользователя: "))
        except ValueError:
            loc_user_id = 171691064
    else:
        loc_user_id = sys.argv[1]
    # Если user_id - строка:
    if isinstance(loc_user_id, str):
        params['user_ids'] = loc_user_id
        loc_response = requests.get('https://api.vk.com/method/users.get', params)
        loc_user_id = loc_response.json()['response'][0]['id']
        print(loc_user_id)
    return loc_user_id


# Получить список id друзей:
def get_friends_id_list(user_id):
    params['user_id'] = user_id
    loc_response = requests.get('https://api.vk.com/method/friends.get', params)
    return loc_response.json()['response']['items']


def get_filtered_user_groups_id(user_id, friends_list_ids):
    friend_groups = []
    # 2. Получаем список id групп пользователя
    params['user_id'] = user_id
    response = requests.get('https://api.vk.com/method/groups.get', params)
    user_groups_ids = response.json()['response']['items']

    i = 0
    ind = 0
    print('Filtering process:')
    # 3. цикл по списку друзей:
    while ind < len(friends_list_ids) - 1:

        # 4. Получаем список групп каждого друга по очереди
        params['user_id'] = friends_list_ids[ind]
        response = requests.get('https://api.vk.com/method/groups.get', params)
        print('*', end='')
        i += 1
        if i % 90 == 0:
            print()
        if 'error' in response.json():
            if response.json()['error']['error_code'] == 6:
                time.sleep(1.6)
                ind -= 1
        else:
            friend_groups = response.json()['response']['items']
        ind += 1
        # 5. Сравнить c со списком групп юзера и удалить дубли
        for user_gr_id in user_groups_ids:
            if user_gr_id in friend_groups:
                user_groups_ids.remove(user_gr_id)
    return user_groups_ids


# Получить инфо о группе по айди
def get_group_info_by_id(group_id, ind):
    group_dict = {}
    params['group_id'] = group_id
    loc_response = requests.get('https://api.vk.com/method/groups.getById', params)

    if 'error' in loc_response.json():
        if loc_response.json()['error']['error_code'] == 6:
            time.sleep(1.6)
            ind -= 1
    else:
        # Получаем значения name, gid и members_count из response:
        gid = group_id
        name = loc_response.json()['response'][0]['name']
        members_count = loc_response.json()['response'][0]['members_count']

        # В словарь  group записывам ключи name, gid, members_count
        group_dict = {'name': name, 'gid': gid, 'members_count': members_count}
    return group_dict, ind


# Получение инфо о группе и запись в файл
# 6. Получаем дополнительное поле - "Число участников группы", с помощью параметра запроса
def user_groups_info_output(user_groups_ids):
    params['fields'] = 'members_count'
    groups_list = []

    # 7. Идем циклом по списку id групп
    ind = 0
    while ind < len(user_groups_ids) - 1:
        gr_id = user_groups_ids[ind]
        groups_list.append(get_group_info_by_id(gr_id, ind))
        ind += 1

    # 8. Запись списка групп в файл
    with open('groups.json', 'w', encoding="utf-8") as fo:
        json.dump(groups_list, fo, ensure_ascii=False)
        print('\nFile groups.json ready')


# 1 Получаем id пользователя в вк
if user_vk_id is None:
    get_input_data()
# 2 Получаем список id друзей
friends_list = get_friends_id_list(user_vk_id)

# 3 Оставляем уникальные
filtered_user_groups_ids = get_filtered_user_groups_id(user_vk_id, friends_list)
# 4 Гет инфо и запись в файл
user_groups_info_output(filtered_user_groups_ids)
