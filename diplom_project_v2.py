import requests
import json
from time import sleep

token = 'e72ded3542717c97e8015eea95cc639641651ba855c9ac1158fe58262fa36274f38945500286a489388bc'
user_id = 175876682
API = 'https://api.vk.com/method'

class User:

    def __init__(self, user_id):
       self.token = token,
       self.user_id = user_id
    
    def get_friends(self, user_id):

        friends_list = []
        params = {
                  'access_token': self.token,
                  'user_id': self.user_id,
                  'v': 5.107,
                  'fields': 'domain'
                  }

        response = requests.get(f'{API}/friends.get', params).json()

        for info in response:
            if 'error' in info:
                print(f'К информации об id={response["error"]["request_params"][0]["value"]} нет доступа')
            else:
                for user in response['response']['items']:
                    if 'deactivated' in user.keys():
                        pass
                    else:
                        friends_list.append(user['id'])

        return friends_list

    def get_user_groups(self):

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
                print(f'К информации об {response["error"]["request_params"][0]["value"]} нет доступа')
            else:
                for group in response['response']['items']:
                    groups_list.append({'gid': group['id'], 'name': group['name'], 'members_count': group['members_count']})

        return groups_list

    def is_member(self, user_id, group_id):

        params = {
              'access_token': self.token,
              'v': 5.107,
              'user_ids': user_id,
              'group_id': group_id,
              }

        response = requests.get(f'{API}/groups.isMember', params)
        
        for info in response.text:
            if 'error' in info:
                print(response)
            else:
                return response.json()

    def main(self):

        friends_list = self.get_friends(user_id)
        user_groups = self.get_user_groups()
        info_list = []
        
        for group in user_groups:
            sleep(0.4)
            some_list = []
            print(f'Обработано групп: {user_groups.index(group)+1} из {len(user_groups)}')
            resp_result = self.is_member(str(friends_list).strip('[]'), group['gid'])['response']
            for item in resp_result:
                if item['member'] == 1:
                    break
                else:
                    some_list.append(item)
            if len(some_list) == len(resp_result):
                info_list.append(group)
                print(group)
            some_list.clear()

        return info_list

if __name__ == '__main__':
    user1 = User(user_id)
    with open('get_difference2.json', 'w', encoding='utf-8') as fo:
        json.dump(user1.main(), fo, ensure_ascii=False, indent=4)
