import requests
import json
from time import sleep

token = 'e72ded3542717c97e8015eea95cc639641651ba855c9ac1158fe58262fa36274f38945500286a489388bc'
user_id = 175876682
##user_id = 1436403
##user_id = 201204
API = 'https://api.vk.com/method'

def get_groups(user_id):

    groups_list = []
    
    params = {
              'access_token': token,
              'user_id': user_id,
              'v': 5.107,
              'extended': 1,
              'fields': ['id', 'name', 'members_count']
              }

    response = requests.get(f'{API}/groups.get', params).json()

    for group in response['response']['items']:
        groups_list.append({'gid': group['id'], 'name': group['name'], 'members_count': group['members_count']})
##        groups_list.append({'gid': group['id'], 'name': group['name']})

##    with open('some_groups_json.json', 'a', encoding='utf8') as f:
##        json.dump(groups_list, f.read().encode('utf8'))

    return groups_list
##    return response['response']['count']

##print(get_groups(user_id))

def get_friends(user_id):

    friends_list = []
    
    params = {
              'access_token': token,
              'user_id': user_id,
              'v': 5.107,
##              'count': 25,
              'fields': 'domain'
              }

    response = requests.get(f'{API}/friends.get', params).json()

    for user in response['response']['items']:
        friends_list.append(user['id'])

    return friends_list

def get_members(group_id):

    members_list = []

    params = {
          'access_token': token,
          'group_id': group_id,
          'v': 5.107,
          'offset': 0,
          'count': 1000,
          'filter': 'friends'
          }

    response = requests.get(f'{API}/groups.getMembers', params=params).json()

##    for member_info in response['response']['items']:
##        with open('some_info.json', 'a', encoding='utf8') as f:
##            json.dump(member_info, f, indent=4, ensure_ascii=False)

    return response

def members_count_info(group_id):

    params = {
      'group_id': group_id,
      'fields': 'members_count',
      'access_token': token,
      'v': 5.107,
      }

    response = requests.get(f'{API}/groups.getById', params=params).json()

    return response

def get_all_members():

    args = ('group')

##    code = '''
##       var group_members = [];
##       var i = 0;
##       var offset = 0;
##       var counter = 0;
##       var groups = API.groups.get({'count':1000}).items;
##       var group = groups[counter];
##       var users = API.groups.getMembers({'group_id': group, 'offset': offset, 'count':1000}).items;
##       var users_count = API.groups.getMembers({'group_id': group, 'offset': offset, 'count':1000}).count;
##       while (i < 22){
##       group_members = group_members + [users];
##       i = i+1;
##       offset = offset + 1000;
##       if (offset > users_count) {
##       counter = counter + 1;
##       };
##       };
##       return group_members;
##       '''

##    code = '''
##       var group_members = [];
##       var i = 0;
##       var offset = 0;
##       var counter = 0;
##       var group = 41633702;
##       var users = API.groups.getMembers({'group_id': group, 'offset': offset, 'count':10}).items;
##       var users_count = API.groups.getMembers({'group_id': group, 'offset': offset, 'count':10}).count;
##       while (i < 22){
##       group_members = group_members + [users];
##       i = i+1;
##       offset = offset + 10;
##       if (offset > users_count) {
##       counter = counter + 1;
##       };
##       };
##       return group_members;
##       '''

    code = '''
       var group_members = [];
       var i = 0;
       var offset = 0;
       var group = 41633702;
       var users = API.groups.getMembers({'group_id': group, 'offset': offset, 'count':10}).items;
       offset = offset + 10;
       while (i < 22){
       group_members = group_members + [users];
       i = i+1;
       offset = offset + 10;
       };
       return group_members;
       '''


##    code = '''
##       var some_list = [];
##       var i = 0;
##       var groups = API.groups.get({'count':1000}).items;
##       var group = groups[i];
##       while (i < 4){
##       some_list = some_list + [group];
##       i = i+1;
##       };
##       return some_list;
##       '''

##    code = '''
##       var members = API.groups.getMembers({'group_id': '1023', 'count':1000}).items;
##       return members;
##       '''
    
    params = {'code': code,
            'access_token': token,
            'v': 5.107,
             }

    response = requests.get(url=f'{API}/execute', params=params).json()

##    for member_info in response['response']['items']:
##        with open('members_info.json', 'a', encoding='utf8') as f:
##            json.dump(member_info, f, indent=4, ensure_ascii=False)

    return response

some_list = []
some_list2 = []

for i in range (1, 6):
    some_list.append(get_all_members()['response'])

##print(len(some_list))

for item in some_list:
    for i in item:
        some_list2.append(i)

print(some_list[0])
print(some_list[1])
##if some_list[0] == some_list[2]:
##    print('Карамба!')
##else:
##    print('Четко!')
##print(len(some_list2))
##
##for a in some_list2:
##    print(len(a))
##print(members_count_info(1023)['response'][0]['members_count'])

##some_list = []

##for item in get_all_members()['response']:
##    sleep(0.4)
##    counter = 0
##    some_list.append(item)
##    if counter < members_count_info(41633702)['response'][0]['members_count']:
##        counter = counter + 1000
##
##for item in some_list:
##    print(len(item))
##print(len(get_all_members()['response']))
##for item in get_all_members()['response']:
##    print(len(item))

##some_list = []
##
##for i in range(1,5):
##    some_list.append(get_all_members()[0]['items'])
##    sleep(0.4)
##
##print(some_list)
