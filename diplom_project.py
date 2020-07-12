import requests
import json
from time import sleep

token = '6a9bda99498b4f3f6ae1e9337335d186761f3e2296205a4266690a4ffcc8ed4a6d56f5deef76da59bb0b9'
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

        try:
            for info in response:
                if 'error' in info:
                    print(f'К информации об id={response["error"]["request_params"][0]["value"]} нет доступа')
                    continue
                
                for user in response['response']['items']:
                    if 'deactivated' not in user.keys():
                        friends_list.append(user['id'])
        except:
            print('Ошибка в методе get_friends')

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

        try:
            for info in response:
                if 'error' in info:
                    print(f'К информации об {response["error"]["request_params"][0]["value"]} нет доступа')
                else:
                    for group in response['response']['items']:
                        groups_list.append({'gid': group['id'], 'name': group['name']})
        except:
            print('Ошибка в методе get_user_groups')

        return groups_list

    def is_member(self, user_id, group_id):

        params = {
              'access_token': self.token,
              'v': 5.107,
              'user_ids': user_id,
              'group_id': group_id,
              }

        response = requests.post(f'{API}/groups.isMember', params)

        try:
            for info in response.text:
                if 'error' in info:
                    print(response)
                else:
                    return response.json()
        except:
            print('Ошибка в методе is_member')

    def get_group_info(self, group_id):

        params = {
              'access_token': self.token,
              'v': 5.107,
              'group_ids': group_id,
              'fields': ['id', 'name', 'members_count']
              }

        response = requests.get(f'{API}/groups.getById', params)

        try:
            for info in response.text:
                
                if 'error' in info:
                    print(response)
                else:
                    return response.json()
        except:
            print('Ошибка в методе get_group_info')


    def main(self):

        friends_list = self.get_friends(user_id)
        user_groups = self.get_user_groups()
        info_list = []
        friends_500_list = []
        full_groups_info = []

        if len(friends_list) > 500:
            for i in range(0, len(friends_list) // 500 + 1):
                friends_500_list.append(friends_list[500*i:500*i+500])
            for group in user_groups:
                sleep(0.4)
                some_list = []
                print(f'Обработано групп: {user_groups.index(group)+1} из {len(user_groups)}')
                try:
                    for friends_list in friends_500_list:
                        sleep(0.4)
                        resp_result = self.is_member(str(friends_list).strip('[]'), group['gid'])
                        if 'error' not in resp_result:
                            for item in resp_result['response']:
                                    if item['member'] == 1:
                                        break
                                    else:
                                        some_list.append(item)
                            if some_list == resp_result['response']:
                                info_list.append(group['gid'])
                                print(group)                            
                        else:
                            print(f'Возникает ошибка: \
"{resp_result["error"]["error_msg"]}" в группе \
id={resp_result["error"]["request_params"][4]["value"]}')
                            break
                except:
                    print('Ошибка в методе main')
        else:
            for group in user_groups:
                sleep(0.4)
                some_list = []
                print(f'Обработано групп: {user_groups.index(group)+1} из {len(user_groups)}')
                try:
                    resp_result = self.is_member(str(friends_list).strip('[]'), group['gid'])
                    if 'error' not in resp_result:
                        for item in resp_result['response']:
                                if item['member'] == 1:
                                    break
                                else:
                                    some_list.append(item)
                        if some_list == resp_result['response']:
                            info_list.append(group['gid'])
                            print(group)                            
                    else:
                        print(f'Возникает ошибка: \
"{resp_result["error"]["error_msg"]}" в группе \
id={resp_result["error"]["request_params"][4]["value"]}')
                        break
                except:
                    print('Ошибка в методе main. После else.')

        groups_info = self.get_group_info(str(info_list).strip('[]'))

        for group in groups_info['response']:
            full_groups_info.append({'gid': group['id'], 'name': group['name'],
                                     'members_count': group['members_count']})
            
        return full_groups_info

if __name__ == '__main__':
    user1 = User(175876682)
    user2 = User(20432421)
    user3 = User(1436403)
    with open('get_difference.json', 'w', encoding='utf-8') as fo:
        json.dump(user1.main(), fo, ensure_ascii=False, indent=4)
    with open('get_difference2.json', 'w', encoding='utf-8') as fo:
        json.dump(user2.main(), fo, ensure_ascii=False, indent=4)
    with open('get_difference3.json', 'w', encoding='utf-8') as fo:
        json.dump(user3.main(), fo, ensure_ascii=False, indent=4)
