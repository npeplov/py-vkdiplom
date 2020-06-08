import time
import requests
# from pprint import pprint

#
#
# не состоит никто из его друзей:
# 1. Получить список друзей friends_ids = [] , цикл
#
# for friend_id in friends_ids:

# 2. Получить список групп каждого друга по очереди groups_ids = []
#     friend_id = 123456789
#     params['user_id'] = friend_id
#     response = requests.get('https://api.vk.com/method/groups.get', params)
#     ids_list = response.json()['response']['items']
# Получим список групп друга [8564, 4100014, 101522128, 134709480, 35486626, 27683540, 125927592]
friend_groups = [8564, 4100014, 101522128, 134709480, 35486626, 27683540, 125927592]
# 3. Сравнить c со списком групп юзера
user_groups_ids = [123, 321, 456, 789, 8564]


for user_gr_id in user_groups_ids:
    if user_gr_id in friend_groups:
        user_groups_ids.remove(user_gr_id)

print(user_groups_ids)
print(friend_groups)


try:
    print('Нажмите Enter, чтобы использовать 171691064')
    user_id = int(input("Введите id пользователя: "))
except ValueError:
    user_id = 171691064


TOKEN = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'
params = {
    'access_token': TOKEN,
    'v': 5.89
}


def get_group_info_by_id(group_id):
    params['group_id'] = group_id
    loc_response = requests.get('https://api.vk.com/method/groups.getById', params)

    # 4.1 Получаем значения name, gid и members_count из response:
    gid = group_id
    name = loc_response.json()['response'][0]['name']
    members_count = loc_response.json()['response'][0]['members_count']

    # 4.2 В словарь  group записывам ключи name, gid, members_count
    group_dict = {'name': name, 'gid': gid, 'members_count': members_count}
    return group_dict


"""""
1. Вывести список групп в ВК в которых состоит пользователь, 
но не состоит никто из его друзей. 

тестировать, можно https://vk.com/eshmargunov

Входные данные:
Имя пользователя или его id в ВК, для которого мы проводим исследование.
Внимание: и имя пользователя (eshmargunov) и id (171691064) 
являются валидными входными данными.

Ввод можно организовать любым способом:
### из консоли
из параметров командной строки при запуске
### из переменной
"""

# 1. Получаем список id групп пользователя
params['user_id'] = user_id
response = requests.get('https://api.vk.com/method/groups.get', params)
ids_list = response.json()['response']['items']
print(ids_list)

# 2. Получаем дополнительное поле - "Число участников группы", с помощью параметра запроса
params['fields'] = 'members_count'

# 3. Открываем файл groups.json на запись
with open('groups.json', 'w', encoding="utf-8") as fo:
    # Записываем скобку
    fo.write('[\n')

    # 4. Идем циклом по списку id групп
    for gr_id in ids_list:
        group_string = str(get_group_info_by_id(gr_id))
        # 4. В файл пишем строку
        fo.write(f'{group_string}\n')
        time.sleep(0.5)

    # Записываем скобку
    fo.write(']')


"""""
Выходные данные:
Файл groups.json в формате:
[
    {
    “name”: “Название группы”, 
    “gid”: “идентификатор группы”, 
    “members_count”: количество_участников_сообщества
    },
    {
    …
    }
]
Форматирование не важно, важно чтобы файл был в формате json
"""""
# groups.getById
# params = { group_id: из списка id, fields: members_count}
# response: name название сообщества. members_count
# screen_name короткий адрес, например, apiclub.
