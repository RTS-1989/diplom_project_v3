import requests
import json
from time import sleep

token = 'e72ded3542717c97e8015eea95cc639641651ba855c9ac1158fe58262fa36274f38945500286a489388bc'
user_id = 175876682
API = 'https://api.vk.com/method'


class User:

    def __init__(self, user_id: int):
        self.token = token
        self.user_id = user_id

    def get_groups(self):

        groups_list = []
        params = {
                  'access_token': self.token,
                  'user_id': self.user_id,
                  'v': 5.107,
                  'extended': 1,
                  'fields': ['id', 'name', 'members_count']
                  }

        response = requests.get(f'{API}/groups.get', params).json()

        for info in response:
            if 'error' in info:
                print(f'К информации об id={response["error"]["request_params"][0]["value"]} нет доступа')
            else:
                for group in response['response']['items']:
                    groups_list.append({'gid': group['id'], 'name': group['name'], 'members_count': group['members_count']})

        return groups_list

    def get_group_difference(self, group_id):

        difference_list = []

        params = {
              'access_token': self.token,
              'group_id': group_id,
              'v': 5.107,
              'filter': 'friends'
              }

        response = requests.get(f'{API}/groups.getMembers', params=params).json()

        for info in response:
            if 'error' in info:
                print(f'К информации об id={response["error"]["request_params"][0]["value"]} нет доступа')
            else:
                return response

    def main(self):

        info_list = []
        
        for group_id in user1.get_groups():
            print(f'Обработано групп: {user1.get_groups().index(group_id)+1} из {len(user1.get_groups())}')
            sleep(0.4)
            condition = user1.get_group_difference(group_id['gid'])['response']['count']
            if condition == 0:
                info_list.append(group_id)
                print(f'Группа {group_id} есть только у id{user_id}')
                
        return info_list


if __name__ == '__main__':
    user1 = User(user_id)
    with open('get_difference.json', 'w', encoding='utf-8') as fo:
        json.dump(user1.main(), fo, ensure_ascii=False, indent=4)
