import json
from json import JSONDecodeError
import constants as cons


def save_user_details(chat_id, dist, age, dose_type):
    data = get_user(chat_id)
    if data is None:
        user_details = dict()
        user_details['dist_id'] = [cons.district_map[dist.lower()]]
        user_details['age'] = int(age)
        user_details['dose_type'] = int(dose_type)

        print('Saving user details....')
        save_user(chat_id, user_details)

    else:
        print('User details found in db')


def save_user(chat_id, user_details):
    with open('users.json', 'r+') as out:
        try:
            data = json.loads(out.read())
        except JSONDecodeError:
            data = {}

        # print("all users: ", data)
        data[str(chat_id)] = user_details
        out.seek(0)
        out.truncate()
        # print('saving: ', data)
        out.write(json.dumps(data))
    print("User details saved....")


def get_user(chat_id):
    with open('users.json', 'r') as f:
        try:
            data = json.loads(f.read())
        except JSONDecodeError:
            data = {}

        if str(chat_id) in data:
            print('User found...')
            return data[str(chat_id)]
        else:
            print('User not found...')
            return None
