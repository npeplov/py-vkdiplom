import json
import time
import requests
import sys

# В константу TOKEN введите токен
TOKEN = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'
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

    ind = 0
    print('Estimated:')
    # 3. цикл по списку друзей:
    while ind < len(friends_list_ids):
        # 4. Получаем список групп каждого друга по очереди
        params['user_id'] = friends_list_ids[ind]
        response = requests.get('https://api.vk.com/method/groups.get', params)
        if 'error' in response.json():
            if response.json()['error']['error_code'] == 6:
                time.sleep(0.8)
                ind -= 1
        else:
            friend_groups = response.json()['response']['items']
        ind += 1
        print('\r\033[K', end='')
        print(len(friends_list) - ind, end='')

        # 5. Сравнить c со списком групп юзера и удалить дубли
        for user_gr_id in user_groups_ids:
            if user_gr_id in friend_groups:
                user_groups_ids.remove(user_gr_id)
    print()
    return user_groups_ids


# Получить инфо о группе по айди
def get_group_info_by_id(group_id):
    group_dict = {}
    params['group_id'] = group_id
    loc_response = requests.get('https://api.vk.com/method/groups.getById', params)

    if 'error' not in loc_response.json():
        # Получаем значения name, gid и members_count из response:
        gid = group_id
        name = loc_response.json()['response'][0]['name']
        members_count = loc_response.json()['response'][0]['members_count']

        # В словарь  group записывам ключи name, gid, members_count
        group_dict = {'name': name, 'gid': gid, 'members_count': members_count}
    return group_dict


# Запись в файл полученной инфо о группе
# 6. Получаем дополнительное поле - "Число участников группы", с помощью параметра запроса
def user_groups_info_output(user_groups_ids):
    params['fields'] = 'members_count'
    groups_list = []

    # 7. Идем циклом по списку id групп
    ind = 0
    while ind < len(user_groups_ids):
        gr_id = user_groups_ids[ind]
        groups_item = get_group_info_by_id(gr_id)
        if groups_item != {}:
            groups_list.append(groups_item)
            ind += 1
        else:
            time.sleep(0.8)

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
