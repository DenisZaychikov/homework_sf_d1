import requests
import json
import sys

key_trello = 'Ваш ключ trello'
token_trello = 'Ваш токен trello'
board_id = 'Ваш ID созданной доски'


def get_lists():  # получить все колонки на доске
    url = f'https://api.trello.com/1/boards/{board_id}/lists'
    params = {'key': key_trello,
              'token': token_trello,
              'fields': 'name'
              }
    columns = requests.get(url, params=params).json()

    return columns


def get_tasks(columns):  # получить список дел по каждой колонке
    params = {'key': key_trello,
              'token': token_trello,
              'fields': 'name'
              }
    for column in columns:
        print(column['name'])
        list_id = column['id']
        url = f'https://api.trello.com/1/lists/{list_id}/cards'
        tasks = requests.get(url, params=params).json()
        if not tasks:
            print('\t' + 'Нет заданий')
            continue
        for task in tasks:
            print('\t' + task['name'])


def count_tasks(columns):  #осчитать количество задач по каждой колонке
    for column in columns:
        for ind, i in enumerate(column['name']):
            if i.isdigit():
                index = ind - 1
                column_name = column['name'][:index]
                break
            else:
                column_name = column['name']
        list_id = column['id']
        url = f'https://api.trello.com/1/lists/{list_id}/cards'
        tasks = requests.get(url, params={'key': key_trello,
                                          'token': token_trello,
                                          'fields': 'name'}).json()
        counter = len(tasks)
        url1 = f'https://api.trello.com/1/lists/{list_id}'
        requests.put(url1, params={'key': key_trello,
                                   'token': token_trello,
                                   'name': f'{column_name} {counter} task(s)'}).json()
                                     

def create_task(task_name, column_name, columns):  # создать задачу в определенной колонке
    for column in columns:
        if column_name in column['name']:
            list_id = column['id']
            break
    params = {'key': key_trello,
              'token': token_trello,
              'name': task_name,
              'idList': list_id}
    url = 'https://api.trello.com/1/cards'

    response = requests.post(url, params=params)


def get_all_tasks():  # получить все задачи, которые на доске 
    url = f'https://api.trello.com/1/boards/{board_id}/cards'
    params = {'key': key_trello,
              'token': token_trello,
              'fields': ['name', 'id']}
    board_tasks = requests.get(url, params=params).json()

    return board_tasks


def move_task(task_name, column_name, columns):  # переместить задачу в другую колонку
    for column in columns:
        if column_name in column['name']:
            new_list_id = column['id']
            break

    board_tasks = get_all_tasks()

    for task in board_tasks:
        if task_name == task['name']:
            card_id = task['id']
            break

    url = f'https://api.trello.com/1/cards/{card_id}/idList'
    params = {'key': key_trello,
              'token': token_trello,
              'value': new_list_id}
    response = requests.put(url, params=params)
    

def create_column(new_column_name): # создать новую колонку
    url = f'https://api.trello.com/1/boards/{board_id}/lists'
    params = {'key': key_trello,
              'token': token_trello,
              'name': new_column_name}
    response = requests.post(url, params=params)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('Вы не выбрали ни одну из команд! Пожалуйста, посмотрите перечень команд в README.md')
    elif sys.argv[1] == 'get_tasks':
        get_tasks(columns)
    elif sys.argv[1] == 'create_task':
        task_name = sys.argv[2]
        column_name = sys.argv[3]
        create_task(task_name, column_name, columns)
    elif sys.argv[1] == 'move_task':
        task_name = sys.argv[2]
        column_name = sys.argv[3]
        move_task(task_name, column_name, columns)
    elif sys.argv[1] == 'create_column':
        new_column_name = sys.argv[2]
        create_column(new_column_name)
    columns = get_lists()    
    count_tasks(columns)
